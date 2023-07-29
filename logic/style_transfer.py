import os

import tensorflow as tf
import cv2 as cv

from enum import Enum

from PyQt6.QtCore import pyqtSignal

from logic.preprocessing import preprocess_image, load_img, convert_opencv_image_to_tensor


class StyleTransfer:
    """Class for logic for style transfer module"""
    class StyleTransferMode(Enum):
        """Enum which defines models used for stylizing, it can be set by set_mode() method"""
        IMAGE = 0,
        VIDEO = 1

    style_predict_image_model_path = None
    style_transform_image_model_path = None
    style_predict_video_model_path = None
    style_transform_video_model_path = None

    active_style_predict_model_path = None
    active_style_transform_model_path = None

    @classmethod
    def set_mode(cls, mode: StyleTransferMode):
        """sets chosen mode as active which means that models proper to that mode will be used for stylizing
        :param mode: enum defining mode"""
        match mode:
            case cls.StyleTransferMode.IMAGE:
                cls.active_style_predict_model_path = cls.style_predict_image_model_path
                cls.active_style_transform_model_path = cls.style_transform_image_model_path
            case cls.StyleTransferMode.VIDEO:
                cls.active_style_predict_model_path = cls.style_predict_video_model_path
                cls.active_style_transform_model_path = cls.style_transform_video_model_path
            case _:
                cls.active_style_predict_model_path = cls.style_predict_video_model_path
                cls.active_style_transform_model_path = cls.style_transform_video_model_path

    @classmethod
    def load_models(cls):
        """should be called at the start of the program, loads all models used for stylization"""
        # models for images
        cls.style_predict_image_model_path = tf.keras.utils.get_file('style_predict.tflite',
                                                                     'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite')

        cls.style_transform_image_model_path = tf.keras.utils.get_file('style_transform.tflite',
                                                                       'https://tfhub.dev/sayakpaul/lite-model/arbitrary-image-stylization-inceptionv3/int8/transfer/1?lite-format=tflite')

        # models for video
        cls.style_predict_video_model_path = tf.keras.utils.get_file('style_predict.tflite',
                                                                     'https://tfhub.dev/sayakpaul/lite-model/arbitrary-image-stylization-inceptionv3/int8/predict/1?lite-format=tflite')

        cls.style_transform_video_model_path = tf.keras.utils.get_file('style_transform.tflite',
                                                                       'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite')

        # set active models
        cls.active_style_predict_model_path = cls.style_predict_video_model_path
        cls.active_style_transform_model_path = cls.style_transform_video_model_path

    @classmethod
    def run_style_predict(cls, preprocessed_style_image):
        """Function to run style prediction on preprocessed style image
        :param preprocessed_style_image: image as a tensor of shape (batch_size=1, width=256, height=256, rgb=3)
        :return: numpy array defining style of an image"""
        interpreter = tf.lite.Interpreter(model_path=cls.active_style_predict_model_path)

        # Set model input.
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]["index"], preprocessed_style_image)

        # Calculate style bottleneck.
        interpreter.invoke()
        style_bottleneck = interpreter.tensor(
            interpreter.get_output_details()[0]["index"])()

        return style_bottleneck

    @classmethod
    def run_style_transform(cls, style_bottleneck, preprocessed_content_image):
        """Run style transform on preprocessed style image
        :param style_bottleneck: numpy array defining style of an image
        :param preprocessed_content_image: image as a tensor of shape (batch_size=1, width=384, height=384, rgb=3)
        :return: result image as numpy array of the same shape as preprocessed_content_image"""
        interpreter = tf.lite.Interpreter(model_path=cls.active_style_transform_model_path)

        # Set model input.
        input_details = interpreter.get_input_details()
        interpreter.allocate_tensors()

        # Set model inputs.
        interpreter.set_tensor(input_details[0]["index"], preprocessed_content_image)
        interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
        interpreter.invoke()

        # Transform content image.
        stylized_image = interpreter.tensor(
            interpreter.get_output_details()[0]["index"]
        )()

        return stylized_image

    @staticmethod
    def stylize_image(content_image, style_image, content_blending_ratio: float):
        """Use active models to stylize an image
        :param content_image: image as a tensor of shape (batch_size=1, width=384, height=384, rgb=3)
        :param style_image: image as a tensor of shape (batch_size=1, width=256, height=256, rgb=3)
        :param content_blending_ratio: how much style of the content image is considered (between 0.0 and 1.0)
        :return result image as numpy array in a shape (width=384, height=384, rgb=3):
        """
        # Calculate style bottleneck for the preprocessed style image.
        style_bottleneck = StyleTransfer.run_style_predict(style_image)
        style_bottleneck_content = StyleTransfer.run_style_predict(preprocess_image(content_image, 256))
        style_bottleneck_blended = content_blending_ratio * style_bottleneck_content + (
                1 - content_blending_ratio) * style_bottleneck

        # Stylize the content image using the style bottleneck.
        result_image = StyleTransfer.run_style_transform(style_bottleneck_blended, content_image)[0]

        return result_image

    @staticmethod
    def stylize_video(content_video_path: str, style_image_path: str, content_blending_ratio: float,
                      progress_signal: pyqtSignal(int)):
        """Use active models to stylize a video
        :param content_video_path: path to video
        :param style_image_path: path to style image
        :param content_blending_ratio: how much style of the content video is considered (between 0.0 and 1.0)
        :param progress_signal: signal to emit every frame
        :return: path to result video
        """
        result_video_path = StyleTransfer.find_next_result_video_path()
        style_image = preprocess_image(load_img(style_image_path), 256)
        video_capture_object = cv.VideoCapture(content_video_path)

        frame_size = (384, 384)
        frame_rate = video_capture_object.get(cv.CAP_PROP_FPS)
        frame_counter = int(video_capture_object.get(cv.CAP_PROP_FRAME_COUNT))
        out = cv.VideoWriter(result_video_path, cv.VideoWriter_fourcc(*'DIVX'), frame_rate, frame_size)

        count = 0
        while True:
            success, image = video_capture_object.read()
            if not success:
                break

            content_image_frame = preprocess_image(convert_opencv_image_to_tensor(image), 384)

            result_image_frame = StyleTransfer.stylize_image(content_image_frame, style_image, content_blending_ratio)
            result_image_frame = cv.normalize(result_image_frame, None, 255, 0, cv.NORM_MINMAX, cv.CV_8U)
            result_image_frame = cv.cvtColor(result_image_frame, cv.COLOR_RGB2BGR)
            out.write(result_image_frame)

            # print frame counter for debugging purposses
            count += 1
            progress_signal.emit(int(count*100/frame_counter))

        out.release()

        return result_video_path

    @staticmethod
    def find_next_result_video_path():
        """Finds next video path to use"""
        directory_path = "assets/results/style-video"

        max_number = 0
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue

                if entry.name[:7] == 'result-':
                    if int(entry.name[7]) > max_number:
                        max_number = int(entry.name[7])

        return f"{directory_path}/result-{max_number+1}.avi"

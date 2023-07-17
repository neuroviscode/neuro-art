import tensorflow as tf
import cv2 as cv

from enum import Enum

from logic.preprocessing import preprocess_image, load_img


class StyleTransfer:
    class StyleTransferMode(Enum):
        IMAGE = 0,
        VIDEO = 1

    style_predict_image_model_path = None
    style_transform_image_model_path = None
    style_predict_video_model_path = None
    style_transform_video_model_path = None

    active_style_predict_model_path = None
    active_style_transform_model_path = None

    @classmethod
    def set_mode(cls, mode):
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
        cls.style_predict_image_model_path = tf.keras.utils.get_file('style_predict.tflite',
                                                                     'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite')

        cls.style_transform_image_model_path = tf.keras.utils.get_file('style_transform.tflite',
                                                                       'https://tfhub.dev/sayakpaul/lite-model/arbitrary-image-stylization-inceptionv3/int8/transfer/1?lite-format=tflite')

        cls.style_predict_video_model_path = tf.keras.utils.get_file('style_predict.tflite',
                                                                     'https://tfhub.dev/sayakpaul/lite-model/arbitrary-image-stylization-inceptionv3/int8/predict/1?lite-format=tflite')

        cls.style_transform_video_model_path = tf.keras.utils.get_file('style_transform.tflite',
                                                                       'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite')

        cls.active_style_predict_model_path = cls.style_predict_video_model_path
        cls.active_style_transform_model_path = cls.style_transform_video_model_path

    # Function to run style prediction on preprocessed style image.
    @classmethod
    def run_style_predict(cls, preprocessed_style_image):
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

    # Run style transform on preprocessed style image
    @classmethod
    def run_style_transform(cls, style_bottleneck, preprocessed_content_image):
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
    def stylize_image(content_image, style_image, content_blending_ratio):
        # Calculate style bottleneck for the preprocessed style image.
        style_bottleneck = StyleTransfer.run_style_predict(style_image)
        style_bottleneck_content = StyleTransfer.run_style_predict(preprocess_image(content_image, 256))
        style_bottleneck_blended = content_blending_ratio * style_bottleneck_content + (
                1 - content_blending_ratio) * style_bottleneck

        # Stylize the content image using the style bottleneck.
        result_image = StyleTransfer.run_style_transform(style_bottleneck_blended, content_image)[0]

        return result_image

    @staticmethod
    def stylize_video(content_video_path, style_image_path, content_blending_ratio):
        style_image = preprocess_image(load_img(style_image_path), 256)
        video_capture_object = cv.VideoCapture(content_video_path)

        frame_size = (384, 384)
        frame_rate = video_capture_object.get(cv.CAP_PROP_FPS)
        out = cv.VideoWriter("assets/results/result_video.avi", cv.VideoWriter_fourcc(*'DIVX'), frame_rate, frame_size)

        count = 0
        while True:
            success, image = video_capture_object.read()
            if not success:
                break

            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image = tf.convert_to_tensor(image, dtype=tf.uint8)
            image = tf.image.convert_image_dtype(image, tf.float32)
            image = image[tf.newaxis, :]
            content_image_frame = preprocess_image(image, 384)

            result_image_frame = StyleTransfer.stylize_image(content_image_frame, style_image, content_blending_ratio)
            result_image_frame = cv.normalize(result_image_frame, None, 255, 0, cv.NORM_MINMAX, cv.CV_8U)
            result_image_frame = cv.cvtColor(result_image_frame, cv.COLOR_RGB2BGR)
            out.write(result_image_frame)

            # print frame counter for debugging purposses
            count += 1
            print(count)

        out.release()

        result_video_path = "assets/results/result_video.avi"

        return result_video_path

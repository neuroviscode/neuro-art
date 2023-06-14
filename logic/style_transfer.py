import tensorflow as tf


class StyleTransfer:
    # Function to run style prediction on preprocessed style image.
    @staticmethod
    def run_style_predict(preprocessed_style_image):
        # Load the model.
        style_predict_path = tf.keras.utils.get_file('style_predict.tflite',
                                                     'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite')
        interpreter = tf.lite.Interpreter(model_path=style_predict_path)

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
    @staticmethod
    def run_style_transform(style_bottleneck, preprocessed_content_image):
        # Load the model.
        style_transform_path = tf.keras.utils.get_file('style_transform.tflite',
                                                       'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite')
        interpreter = tf.lite.Interpreter(model_path=style_transform_path)

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

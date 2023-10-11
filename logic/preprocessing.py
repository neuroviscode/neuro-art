import tensorflow as tf
import cv2 as cv
import urllib


def load_img(path_to_img: str):
    """ Function to load an image from a file, and add a batch dimension
    :param path_to_img
    :return image with added batch dimension:
    """
    img = tf.io.read_file(path_to_img)
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]

    return img


def load_img_from_url(url: str):
    """ Function to load an image from an url, and add a batch dimension
        :param url
        :return image with added batch dimension:
        """
    img = urllib.request.urlopen(url).read()
    img = tf.io.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]

    return img


def preprocess_image(image, target_dim: int):
    """ Function to pre-process image by resizing and central cropping it
    :param image: image as a tensor with batch dimension
    :param target_dim: 256 for style image and 384 for content image
    """
    # Resize the image so that the shorter dimension becomes target dimension.
    shape = tf.cast(tf.shape(image)[1:-1], tf.float32)
    short_dim = min(shape)
    scale = target_dim / short_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    image = tf.image.resize(image, new_shape)

    # Central crop the image.
    image = tf.image.resize_with_crop_or_pad(image, target_dim, target_dim)

    return image


def convert_opencv_image_to_tensor(image):
    """Convert loaded opencv image to tensor with batch dimension and RGB values between 0.0 and 1.0
    :param image: opencv image in with BGR color coding"""
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = tf.convert_to_tensor(image, dtype=tf.uint8)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = image[tf.newaxis, :]
    return image


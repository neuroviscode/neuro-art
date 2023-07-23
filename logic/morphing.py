import os
import sys

import cv2
import numpy as np
import tensorflow as tf
from tqdm import tqdm

from tensorflow_addons.image.dense_image_warp import dense_image_warp

ORIG_WIDTH = 0
ORIG_HEIGHT = 0
TRAIN_EPOCHS = 500

im_sz = 1024
mp_sz = 96

warp_scale = 0.05
mult_scale = 0.4
add_scale = 0.4
add_first = False


@tf.function
def warp(origins, targets, preds_org, preds_trg):
    if add_first:
        res_targets = dense_image_warp(
            (origins + preds_org[:, :, :, 3:6] * 2 * add_scale) * tf.maximum(0.1, 1 + preds_org[:, :, :, 0:3] * mult_scale), # noqa E501
            preds_org[:, :, :, 6:8] * im_sz * warp_scale)
        res_origins = dense_image_warp(
            (targets + preds_trg[:, :, :, 3:6] * 2 * add_scale) * tf.maximum(0.1, 1 + preds_trg[:, :, :, 0:3] * mult_scale), # noqa E501
            preds_trg[:, :, :, 6:8] * im_sz * warp_scale)
    else:
        res_targets = dense_image_warp(
            origins * tf.maximum(0.1, 1 + preds_org[:, :, :, 0:3] * mult_scale) + preds_org[:, :, :, 3:6] * 2 * add_scale,  # noqa E501
            preds_org[:, :, :, 6:8] * im_sz * warp_scale)
        res_origins = dense_image_warp(
            targets * tf.maximum(0.1, 1 + preds_trg[:, :, :, 0:3] * mult_scale) + preds_trg[:, :, :, 3:6] * 2 * add_scale,  # noqa E501
            preds_trg[:, :, :, 6:8] * im_sz * warp_scale)

    return res_targets, res_origins


def create_grid(scale):
    grid = np.mgrid[0:scale, 0:scale] / (scale - 1) * 2 - 1
    grid = np.swapaxes(grid, 0, 2)
    grid = np.expand_dims(grid, axis=0)
    return grid


def produce_warp_maps(origins, targets):
    class MyModel(tf.keras.Model):
        def __init__(self):
            super(MyModel, self).__init__()
            self.conv1 = tf.keras.layers.Conv2D(64, (5, 5))
            self.act1 = tf.keras.layers.LeakyReLU(alpha=0.2)
            self.conv2 = tf.keras.layers.Conv2D(64, (5, 5))
            self.act2 = tf.keras.layers.LeakyReLU(alpha=0.2)
            self.convo = tf.keras.layers.Conv2D((3 + 3 + 2) * 2, (5, 5))

        def call(self, maps):
            x = tf.image.resize(maps, [mp_sz, mp_sz])
            x = self.conv1(x)
            x = self.act1(x)
            x = self.conv2(x)
            x = self.act2(x)
            x = self.convo(x)
            return x

    model = MyModel()

    loss_object = tf.keras.losses.MeanSquaredError()
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0002)

    train_loss = tf.keras.metrics.Mean(name='train_loss')

    @tf.function
    def train_step(maps, origins, targets):
        with tf.GradientTape() as tape:
            preds = model(maps)
            preds = tf.image.resize(preds, [im_sz, im_sz])

            # a = tf.random.uniform([maps.shape[0]])
            # res_targets, res_origins = warp(origins, targets, preds[...,:8] * a, preds[...,8:] * (1 - a))
            res_targets_, res_origins_ = warp(origins, targets, preds[..., :8], preds[..., 8:])

            # warp maps consistency checker
            res_map = dense_image_warp(maps, preds[:, :, :, 6:8] * im_sz * warp_scale)
            res_map = dense_image_warp(res_map, preds[:, :, :, 14:16] * im_sz * warp_scale)

            loss = loss_object(maps, res_map) * 1 + \
                   loss_object(res_targets_, targets) * 0.3 + \
                   loss_object(res_origins_, origins) * 0.3

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        train_loss(loss)

    maps = create_grid(im_sz)
    maps = np.concatenate((maps, origins * 0.1, targets * 0.1), axis=-1).astype(np.float32)

    epoch = 0
    template = 'Epoch {}, Loss: {}'

    t = tqdm(range(TRAIN_EPOCHS), desc=template.format(epoch, train_loss.result()))

    for i in t:
        epoch = i + 1

        t.set_description(template.format(epoch, train_loss.result()))
        t.refresh()

        train_step(maps, origins, targets)

        if (epoch < 100 and epoch % 10 == 0) or \
                (epoch < 1000 and epoch % 100 == 0) or \
                (epoch % 1000 == 0):
            preds = model(maps, training=False)[:1]
            preds = tf.image.resize(preds, [im_sz, im_sz])

    return preds


def generate_frames(origins, targets, preds, steps=100):
    # apply maps
    org_strength = tf.reshape(tf.range(steps, dtype=tf.float32), [steps, 1, 1, 1]) / (steps - 1)
    trg_strength = tf.reverse(org_strength, axis=[0])

    frames = []
    for i in tqdm(range(steps)):
        preds_org = preds * org_strength[i]
        preds_trg = preds * trg_strength[i]

        res_targets, res_origins = warp(origins, targets, preds_org[..., :8], preds_trg[..., 8:])
        res_targets = tf.clip_by_value(res_targets, -1, 1)
        res_origins = tf.clip_by_value(res_origins, -1, 1)

        results = res_targets * trg_strength[i] + res_origins * org_strength[i]
        res_numpy = results.numpy()

        img = ((res_numpy[0] + 1) * 127.5).astype(np.uint8)
        frames.append(img)

    return frames


def download_data() -> tuple:
    source = tf.keras.utils.get_file(os.getcwd() + "/assets/examples/morphing_example_1.jpg",
                                     "https://raw.githubusercontent.com/volotat/DiffMorph/master/images/img_3.jpg")
    target = tf.keras.utils.get_file(os.getcwd() + "/assets/examples/morphing_example_2.jpg",
                                     "https://raw.githubusercontent.com/volotat/DiffMorph/master/images/img_4.jpg")
    return source, target


def training(source, target):
    dom_a = cv2.imread(source, cv2.IMREAD_COLOR)
    dom_b = cv2.imread(target, cv2.IMREAD_COLOR)

    # Checks if input and destination image are of the same dimensions.
    if dom_a.shape[1] != dom_b.shape[1] or dom_a.shape[0] != dom_b.shape[0]:
        resulting_shape = (min(dom_a.shape[0], dom_b.shape[0]), min(dom_a.shape[1], dom_b.shape[1]))

        dom_a = cv2.resize(dom_a, resulting_shape)
        dom_b = cv2.resize(dom_b, resulting_shape)

    # Store original height and width
    ORIG_WIDTH = dom_a.shape[1]
    ORIG_HEIGHT = dom_a.shape[0]

    dom_a = cv2.cvtColor(dom_a, cv2.COLOR_BGR2RGB)
    dom_a = cv2.resize(dom_a, (im_sz, im_sz), interpolation=cv2.INTER_AREA)
    dom_a = dom_a / 127.5 - 1

    dom_b = cv2.cvtColor(dom_b, cv2.COLOR_BGR2RGB)
    dom_b = cv2.resize(dom_b, (im_sz, im_sz), interpolation=cv2.INTER_AREA)
    dom_b = dom_b / 127.5 - 1

    origins = dom_a.reshape(1, im_sz, im_sz, 3).astype(np.float32)
    targets = dom_b.reshape(1, im_sz, im_sz, 3).astype(np.float32)

    return produce_warp_maps(origins, targets), origins, targets


def morphing_handler(image_left_path='', image_right_path=''):

    if not image_left_path and not image_right_path:
        image_left_path, image_right_path = download_data()

    predictions, origins, targets = training(image_left_path, image_right_path)

    steps = 50
    frames = generate_frames(origins, targets, predictions, steps)  # generate frames between source and target images

    return frames


if __name__ == "__main__":
    morphing_handler()

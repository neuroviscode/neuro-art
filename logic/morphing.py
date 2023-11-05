import os
import sys

import cv2
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from PyQt6.QtCore import pyqtSignal
from tqdm import tqdm

ORIG_WIDTH = 0
ORIG_HEIGHT = 0

im_sz = 1024
mp_sz = 96

warp_scale = 0.05
mult_scale = 0.4
add_scale = 0.4
add_first = False


@tf.function
def warp(origins, targets, preds_org, preds_trg):
    if add_first:
        res_targets = tfa.image.dense_image_warp(
            (origins + preds_org[:, :, :, 3:6] * 2 * add_scale)
            * tf.maximum(0.1, 1 + preds_org[:, :, :, 0:3] * mult_scale),
            preds_org[:, :, :, 6:8] * im_sz * warp_scale)
        res_origins = tfa.image.dense_image_warp(
            (targets + preds_trg[:, :, :, 3:6] * 2 * add_scale)
            * tf.maximum(0.1, 1 + preds_trg[:, :, :, 0:3] * mult_scale),
            preds_trg[:, :, :, 6:8] * im_sz * warp_scale)
    else:
        res_targets = tfa.image.dense_image_warp(
            origins * tf.maximum(
                0.1, 1 + preds_org[:, :, :, 0:3] * mult_scale) + preds_org[:, :, :, 3:6] * 2 * add_scale,
                preds_org[:, :, :, 6:8] * im_sz * warp_scale)
        res_origins = tfa.image.dense_image_warp(
            targets * tf.maximum(
                0.1, 1 + preds_trg[:, :, :, 0:3] * mult_scale) + preds_trg[:, :, :, 3:6] * 2 * add_scale,
                preds_trg[:, :, :, 6:8] * im_sz * warp_scale)

    return res_targets, res_origins


def create_grid(scale):
    grid = np.mgrid[0:scale, 0:scale] / (scale - 1) * 2 - 1
    grid = np.swapaxes(grid, 0, 2)
    grid = np.expand_dims(grid, axis=0)
    return grid


def produce_warp_maps(origins, targets, progress_signal: pyqtSignal(int)):
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
            res_map = tfa.image.dense_image_warp(maps, preds[:, :, :, 6:8] * im_sz * warp_scale)
            res_map = tfa.image.dense_image_warp(res_map, preds[:, :, :, 14:16] * im_sz * warp_scale)

            loss = loss_object(maps, res_map) * 1 + loss_object(res_targets_, targets) * 0.3 + loss_object(res_origins_,
                                                                                                           origins) * 0.3

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        train_loss(loss)

    maps = create_grid(im_sz)
    maps = np.concatenate((maps, origins * 0.1, targets * 0.1), axis=-1).astype(np.float32)

    epoch = 0
    template = 'Epoch {}, Loss: {}'

    t = tqdm(range(int(os.getenv("TRAIN_EPOCHS"))), desc=template.format(epoch, train_loss.result()))

    for i in t:
        epoch = i + 1

        # t.set_description(template.format(epoch, train_loss.result()))
        # t.refresh()

        train_step(maps, origins, targets)

        progress_signal.emit(int(i * 100 / int(os.getenv("TRAIN_EPOCHS"))))

        if (epoch < 100 and epoch % 10 == 0) or \
                (epoch < 1000 and epoch % 100 == 0) or \
                (epoch % 1000 == 0):
            preds = model(maps, training=False)[:1]
            preds = tf.image.resize(preds, [im_sz, im_sz])

    progress_signal.emit(int(100))

    return preds


def generate_frames(origins, targets, preds, progress_signal: pyqtSignal(int), steps=100):
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
        progress_signal.emit(int(i * 100 / steps))

    progress_signal.emit(int(100))

    return frames


def crop_different_dims_pictures(pic_a, pic_b):
    desired_width = max(pic_a.shape[1], pic_b.shape[1])
    desired_height = max(pic_a.shape[0], pic_b.shape[0])

    image_a_resized = cv2.resize(pic_a, (desired_width, desired_height))
    image_b_resized = cv2.resize(pic_b, (desired_width, desired_height))

    # crop images if the ratios are different
    if image_a_resized.shape != image_b_resized.shape:
        crop_x = (image_a_resized.shape[1] - desired_width) // 2
        crop_y = (image_a_resized.shape[0] - desired_height) // 2
        image_a_resized = image_a_resized[crop_y:crop_y + desired_height, crop_x:crop_x + desired_width]
        image_b_resized = image_b_resized[crop_y:crop_y + desired_height, crop_x:crop_x + desired_width]

    return image_a_resized, image_b_resized


def training(source, target, progress_signal: pyqtSignal(int)):
    dom_a = cv2.imread(os.path.relpath(source), cv2.IMREAD_COLOR)
    dom_b = cv2.imread(os.path.relpath(target), cv2.IMREAD_COLOR)

    if dom_a is None or dom_b is None:
        print(f"Couldn't load images: {dom_a}, {dom_b}")

    # Checks if input and destination image are of the same dimensions.
    if dom_a.shape[1] != dom_b.shape[1] or dom_a.shape[0] != dom_b.shape[0]:
        print("Input Image is not the same dimensions as Destination Image.")
        dom_a, dom_b = crop_different_dims_pictures(dom_a, dom_b)

    # Store original height and width
    dom_a = cv2.cvtColor(dom_a, cv2.COLOR_BGR2RGB)
    dom_a = cv2.resize(dom_a, (im_sz, im_sz), interpolation=cv2.INTER_AREA)
    dom_a = dom_a / 127.5 - 1

    dom_b = cv2.cvtColor(dom_b, cv2.COLOR_BGR2RGB)
    dom_b = cv2.resize(dom_b, (im_sz, im_sz), interpolation=cv2.INTER_AREA)
    dom_b = dom_b / 127.5 - 1

    origins = dom_a.reshape(1, im_sz, im_sz, 3).astype(np.float32)
    targets = dom_b.reshape(1, im_sz, im_sz, 3).astype(np.float32)

    print("Training...")
    return produce_warp_maps(origins, targets, progress_signal), origins, targets


def morphing_handler(
        src_path_1: str,
        src_path_2: str,
        training_signal: pyqtSignal(int),
        morphing_signal: pyqtSignal(int)):

    predictions, origins, targets = training(src_path_1, src_path_2, training_signal)
    steps = int(os.getenv("MORPHING_STEPS"))

    frames = generate_frames(origins, targets, predictions, morphing_signal, steps)  # generate frames between source and target images

    return frames

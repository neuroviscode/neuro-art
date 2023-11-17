import logging
import os
import random
from io import BytesIO

import requests
import urllib
from pathlib import Path

import tensorflow as tf
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSlider, QFileDialog, \
    QCheckBox
from PIL import Image

from logic.preprocessing import preprocess_image, load_img, load_img_from_url
from logic.style_transfer import StyleTransfer
from logic.style_transfer_vae import StyleTransferVAE


class StyleImageMenu(QWidget):
    """Class defining GUI for image style transfer module"""

    num_of_results = 0

    STYLE_IMAGE_RESULTS = 'assets/results/style-image'

    is_content_image_from_url = False
    is_style_image_from_url = False

    def __init__(self):

        super().__init__()

        StyleImageMenu.search_for_results()

        self.style_transformer_vae = StyleTransferVAE()
        self.use_vae_style_transformer = False

        layout = QHBoxLayout()
        self.setLayout(layout)

        left_container = QWidget()
        right_container = QWidget()
        # left_container.setStyleSheet('border: 1px solid blue')
        # right_container.setStyleSheet('border: 1px solid green')
        layout.addWidget(left_container)
        layout.addWidget(right_container)
        layout.setStretch(0, 2)
        layout.setStretch(1, 2)

        self.right_menu = RightMenu()
        layout.addWidget(self.right_menu)

        # left container
        upper_stylization_container = QWidget()
        lower_stylization_container = QWidget()
        left_container_layout = QVBoxLayout()
        left_container_layout.addWidget(upper_stylization_container)
        left_container_layout.addStretch()
        left_container_layout.addWidget(lower_stylization_container)
        left_container.setLayout(left_container_layout)

        # upper stylization container
        upper_stylization_buttons_container = QWidget()
        upper_stylization_image_container = QWidget()
        upper_stylization_container_layout = QHBoxLayout()
        upper_stylization_container_layout.addWidget(upper_stylization_buttons_container)
        upper_stylization_container_layout.addWidget(upper_stylization_image_container)
        upper_stylization_container_layout.setStretch(0, 1)
        upper_stylization_container.setLayout(upper_stylization_container_layout)

        # lower stylization container
        lower_stylization_buttons_container = QWidget()
        lower_stylization_image_container = QWidget()
        lower_stylization_container_layout = QHBoxLayout()
        lower_stylization_container_layout.addWidget(lower_stylization_buttons_container)
        lower_stylization_container_layout.addWidget(lower_stylization_image_container)
        lower_stylization_container_layout.setStretch(0, 1)
        lower_stylization_container.setLayout(lower_stylization_container_layout)

        # upper stylization buttons container
        upper_stylization_buttons_open_file_button = StyleButton(label='Open File',
                                                                 icon_image_path='assets/icons/document.png',
                                                                 button_name='upper_open_button',
                                                                 callback=self.open_content_image_from_file)
        upper_stylization_buttons_select_button = StyleButton(label="Select From Library",
                                                              icon_image_path='assets/icons/bookmark.png',
                                                              button_name='upper_library_button')
        upper_stylization_buttons_wikiart_button = StyleButton(label="Random WikiArt Image",
                                                               icon_image_path='assets/icons/shuffle.png',
                                                               button_name='upper_wikiart_button',
                                                               callback=self.open_random_wikiart_content_image)
        upper_stylization_buttons_layout = QVBoxLayout()
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_open_file_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_select_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_wikiart_button)
        upper_stylization_buttons_layout.addStretch()
        upper_stylization_buttons_container.setLayout(upper_stylization_buttons_layout)

        # upper stylization image container
        self.upper_stylization_image = QLabel()
        self.upper_stylization_image_path = 'assets/examples/golden-gate-example.jpg'
        pixmap = QPixmap(self.upper_stylization_image_path)
        self.upper_stylization_image.setPixmap(pixmap)
        self.upper_stylization_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upper_stylization_image.setFixedSize(pixmap.size())
        self.upper_stylization_image.setObjectName('upper_stylization_image')
        upper_stylization_container_layout.addWidget(self.upper_stylization_image)

        # lower stylization buttons container
        lower_stylization_buttons_open_file_button = StyleButton(label='Open File',
                                                                 icon_image_path='assets/icons/document.png',
                                                                 button_name='lower_open_button',
                                                                 callback=self.open_style_image_from_file)
        lower_stylization_buttons_select_button = StyleButton(label="Select From Library",
                                                              icon_image_path='assets/icons/bookmark.png',
                                                              button_name='lower_library_button')
        lower_stylization_buttons_wikiart_button = StyleButton(label="Random WikiArt Image",
                                                               icon_image_path='assets/icons/shuffle.png',
                                                               button_name='lower_wikiart_button',
                                                               callback=self.open_random_wikiart_style_image)
        lower_stylization_buttons_layout = QVBoxLayout()
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_open_file_button)
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_select_button)
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_wikiart_button)
        lower_stylization_buttons_layout.addStretch()
        lower_stylization_buttons_container.setLayout(lower_stylization_buttons_layout)

        # lower stylization image container
        self.lower_stylization_image = QLabel()
        self.lower_stylization_image_path = 'assets/examples/towers-example.jpg'
        pixmap = QPixmap(self.lower_stylization_image_path)
        self.lower_stylization_image.setPixmap(pixmap)
        self.lower_stylization_image.setObjectName('lower_stylization_image')
        self.lower_stylization_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lower_stylization_image.setFixedSize(pixmap.size())
        lower_stylization_container_layout.addWidget(self.lower_stylization_image)

        # right container
        right_container_layout = QVBoxLayout()
        right_container.setLayout(right_container_layout)
        stylization_controls_container = QWidget()
        result_image_container = QWidget()
        result_controls_container = QWidget()
        right_container_layout.addWidget(stylization_controls_container)
        right_container_layout.addWidget(result_image_container)
        right_container_layout.addWidget(result_controls_container)
        right_container_layout.setStretch(0, 1)
        right_container_layout.setStretch(2, 1)

        # stylization_controls_container
        stylization_controls_container_layout = QVBoxLayout()
        stylization_controls_container.setLayout(stylization_controls_container_layout)

        self.stylization_slider = QSlider()
        self.stylization_slider.setOrientation(Qt.Orientation.Horizontal)
        self.stylization_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.stylization_slider.setValue(60)
        self.stylization_slider.setMinimum(0)
        self.stylization_slider.setMaximum(100)
        self.stylization_slider.setSingleStep(1)
        stylization_controls_container_layout.addWidget(self.stylization_slider)

        self.stylization_switch_container = QWidget()
        self.stylization_switch_container_layout = QHBoxLayout()
        self.stylization_model_switch = QCheckBox()
        self.stylization_model_switch.setChecked(False)
        self.stylization_model_switch.stateChanged.connect(self.toggle_stylization_model)
        self.stylization_switch_text = QLabel('Korzystaj z modelu VAE do stylizacji')
        self.stylization_switch_container_layout.addWidget(self.stylization_switch_text)
        self.stylization_switch_container_layout.addWidget(self.stylization_model_switch)
        self.stylization_switch_container.setLayout(self.stylization_switch_container_layout)
        stylization_controls_container_layout.addWidget(self.stylization_switch_container)

        stylize_button = QPushButton('Stylize')
        icon = QIcon(QPixmap('assets/icons/shuffle.png'))
        stylize_button.setIcon(icon)
        stylize_button.clicked.connect(self.stylize_button_click)
        stylization_controls_container_layout.addWidget(stylize_button)

        # result_image_container
        result_image_container_layout = QVBoxLayout()
        self.result_image = QLabel()
        self.result_image_path = 'assets/examples/style-transfer-result-example.png'
        self.result_image.setPixmap(QPixmap(self.result_image_path))
        result_image_container_layout.addWidget(self.result_image)
        result_image_container.setLayout(result_image_container_layout)

        # result_controls_container
        result_controls_layout = QGridLayout()
        result_save_library_button = StyleButton('Save To Library', 'assets/icons/book.png')
        result_controls_layout.addWidget(result_save_library_button, 0, 1)
        result_controls_layout.setColumnStretch(0, 1)
        result_controls_layout.setRowStretch(1, 1)
        result_controls_container.setLayout(result_controls_layout)

    def toggle_stylization_model(self, state):
        self.use_vae_style_transformer = state

    def stylize_button_click(self):
        """Callback to stylize button"""
        StyleTransfer.set_mode(StyleTransfer.StyleTransferMode.IMAGE)  # set proper stylization models as active
        content_image_path = self.upper_stylization_image_path
        style_image_path = self.lower_stylization_image_path

        if self.use_vae_style_transformer:
            self.stylize_vae_algorithm(content_image_path, style_image_path)
        else:
            self.stylize_classic_algorithm(content_image_path, style_image_path)

        pixmap = QPixmap(self.result_image_path)
        scaled_pixmap = pixmap.scaled(self.result_image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.result_image.setPixmap(scaled_pixmap)

        StyleImageMenu.num_of_results += 1
        self.right_menu.add_recent_artwork(self.result_image_path)

    def stylize_classic_algorithm(self, content_image_path: str, style_image_path: str):
        if self.is_content_image_from_url:
            content_image = preprocess_image(load_img_from_url(content_image_path), 384)
        else:
            content_image = preprocess_image(load_img(content_image_path), 384)

        if self.is_style_image_from_url:
            style_image = preprocess_image(load_img_from_url(style_image_path), 256)
        else:
            style_image = preprocess_image(load_img(style_image_path), 256)

        content_blending_ratio = (100 - self.stylization_slider.value()) / 100  # define content blending ratio between [0..1].

        result_image = StyleTransfer.stylize_image(content_image, style_image, content_blending_ratio)
        self.result_image_path = f'{StyleImageMenu.STYLE_IMAGE_RESULTS}/result-{StyleImageMenu.num_of_results}.png'
        tf.keras.utils.save_img(self.result_image_path, result_image)

    def stylize_vae_algorithm(self, content_image_path: str, style_image_path: str):
        if self.is_content_image_from_url:
            response = requests.get(content_image_path)
            response.raise_for_status()
            content_image = Image.open(BytesIO(response.content))
        else:
            content_image = Image.open(content_image_path).convert('RGB')

        if self.is_style_image_from_url:
            response = requests.get(style_image_path)
            response.raise_for_status()
            style_image = Image.open(BytesIO(response.content))
        else:
            style_image = Image.open(style_image_path).convert('RGB')

        result_image = self.style_transformer_vae.run_style_transfer(content_image, style_image)

        self.result_image_path = f'{StyleImageMenu.STYLE_IMAGE_RESULTS}/result-{StyleImageMenu.num_of_results}.png'

        result_image.save(self.result_image_path)

    def open_content_image_from_file(self) -> None:
        """Callback to open button"""
        file = QFileDialog.getOpenFileName(self, 'Select an image', '.', 'Images (*.png *.jpg)')
        if file:
            if file[0] == '':
                return
            pixmap = QPixmap(file[0])
            self.upper_stylization_image_path = file[0]
            scaled_pixmap = pixmap.scaled(self.upper_stylization_image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.upper_stylization_image.setPixmap(scaled_pixmap)
            self.is_content_image_from_url = False

    def open_style_image_from_file(self) -> None:
        """Callback to open button"""
        file = QFileDialog.getOpenFileName(self, 'Select an image', '.', 'Images (*.png *.jpg)')
        if file:
            if file[0] == '':
                return
            pixmap = QPixmap(file[0])
            self.lower_stylization_image_path = file[0]
            scaled_pixmap = pixmap.scaled(self.lower_stylization_image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.lower_stylization_image.setPixmap(scaled_pixmap)
            self.is_style_image_from_url = False

    def open_random_wikiart_content_image(self) -> None:
        """Callback to random wikiArt image button"""
        loading_succeded = False
        while not loading_succeded:
            response = requests.get('https://www.wikiart.org/en/App/Painting/MostViewedPaintings')
            response.raise_for_status()
            random_image_url = random.choice([x['image'] for x in response.json()])
            try:
                data = urllib.request.urlopen(random_image_url).read()
                loading_succeded = True
            except:
                continue
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaled_pixmap = pixmap.scaled(self.lower_stylization_image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.upper_stylization_image.setPixmap(scaled_pixmap)
        self.upper_stylization_image_path = random_image_url
        self.is_content_image_from_url = True

    def open_random_wikiart_style_image(self) -> None:
        """Callback to random wikiArt image button"""
        loading_succeded = False
        while not loading_succeded:
            response = requests.get('https://www.wikiart.org/en/App/Painting/MostViewedPaintings')
            response.raise_for_status()
            random_image_url = random.choice([x['image'] for x in response.json()])
            try:
                data = urllib.request.urlopen(random_image_url).read()
                loading_succeded = True
            except:
                continue
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaled_pixmap = pixmap.scaled(self.lower_stylization_image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.lower_stylization_image.setPixmap(scaled_pixmap)
        self.lower_stylization_image_path = random_image_url
        self.is_style_image_from_url = True

    @staticmethod
    def search_for_results():
        file_names = []

        logger = logging.getLogger()

        if not os.path.exists(StyleImageMenu.STYLE_IMAGE_RESULTS):
            logger.warning(f'Path to results {StyleImageMenu.STYLE_IMAGE_RESULTS} does not exist')
            logger.warning('Creating the directory...')

            style_image_results_path = Path(StyleImageMenu.STYLE_IMAGE_RESULTS)
            style_image_results_path.mkdir(parents=True)

        with os.scandir(StyleImageMenu.STYLE_IMAGE_RESULTS) as entries:
            for entry in entries:
                if not entry.is_file():
                    continue

                if entry.name[:7] == 'result-' and entry.name.endswith('.png'):
                    file_names.append(entry.name)

        if len(file_names) <= 0:
            StyleImageMenu.num_of_results = 0
            return

        StyleImageMenu.num_of_results = len(file_names)


class RightMenu(QWidget):
    """Class defining GUI for right menu with recent artworks"""
    def __init__(self):
        super().__init__()

        self.right_menu_layout = QVBoxLayout()
        self.setLayout(self.right_menu_layout)
        self.artworks_paths = []

        self.right_menu_layout.addWidget(QLabel('Recent artworks'))

        for i in range(0, 5):
            image = QLabel()
            image.setObjectName('right-menu-artwork')
            image.setFixedSize(120, 120)
            pixmap = QPixmap()
            scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            image.setPixmap(QPixmap(scaled_pixmap))
            self.right_menu_layout.addWidget(image)

        images = self.findChildren(QLabel, 'right-menu-artwork')

        if StyleImageMenu.num_of_results < 5:
            for i in range(StyleImageMenu.num_of_results):
                if os.path.exists(f'{StyleImageMenu.STYLE_IMAGE_RESULTS}/result-{i}.png'):
                    self.artworks_paths.insert(0, f'{StyleImageMenu.STYLE_IMAGE_RESULTS}/result-{i}.png')
                    pixmap = QPixmap(f'{StyleImageMenu.STYLE_IMAGE_RESULTS}/result-{i}.png')
                    scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)
                    images[StyleImageMenu.num_of_results - i - 1].setPixmap(QPixmap(scaled_pixmap))
            return

        for i in range(StyleImageMenu.num_of_results, StyleImageMenu.num_of_results - 5, -1):
            image = QLabel()
            image.setObjectName('right-menu-artwork')
            image.setFixedSize(120, 120)

            self.artworks_paths.insert(0, f'{StyleImageMenu.STYLE_IMAGE_RESULTS}/result-{i}.png')

            pixmap = QPixmap(f'{StyleImageMenu.STYLE_IMAGE_RESULTS}/result-{i - 1}.png')
            scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            images[StyleImageMenu.num_of_results - i] .setPixmap(QPixmap(scaled_pixmap))

        self.right_menu_layout.addStretch()

    def add_recent_artwork(self, artwork_path):

        self.artworks_paths.insert(0, artwork_path)
        if len(self.artworks_paths) > 5:
            self.artworks_paths = self.artworks_paths[:-1]

        images = self.findChildren(QLabel, 'right-menu-artwork')
        for i in range(min(5, StyleImageMenu.num_of_results)):
            pixmap = QPixmap(self.artworks_paths[i])
            scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            images[i].setPixmap(QPixmap(scaled_pixmap))


class StyleButton(QPushButton):

    def __init__(self, label: str, icon_image_path: str, button_name: str = '', callback=None):
        """
        :param label: text to put on the button
        :param icon_image_path: path to icon image
        :param button_name: object name
        :param callback: function to call on button click event
        """
        super().__init__()

        icon = QIcon(QPixmap(icon_image_path))
        self.setIcon(icon)
        self.setText(label)
        self.setStyleSheet('text-align: left; padding: 5px')
        self.setObjectName(button_name)
        if callback:
            self.clicked.connect(callback)

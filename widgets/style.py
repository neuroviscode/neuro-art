import cv2 as cv
import tensorflow as tf
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSlider, QFileDialog

from logic.preprocessing import preprocess_image, load_img
from logic.style_transfer import StyleTransfer


class StyleMenu(QWidget):
    def __init__(self):
        super().__init__()

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

        layout.addWidget(RightMenu())

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
        upper_stylization_buttons_open_file_button = StyleButton('Open File', 'assets/icons/document.png',
                                                                 'upper_open_button')
        upper_stylization_buttons_select_button = StyleButton("Select From Library", 'assets/icons/bookmark.png',
                                                              'upper_library_button')
        upper_stylization_buttons_wikiart_button = StyleButton("Random WikiArt Image", 'assets/icons/shuffle.png',
                                                               'upper_wikiart_button')
        upper_stylization_buttons_layout = QVBoxLayout()
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_open_file_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_select_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_wikiart_button)
        upper_stylization_buttons_layout.addStretch()
        upper_stylization_buttons_container.setLayout(upper_stylization_buttons_layout)

        # upper stylization image container
        upper_stylization_image = QLabel()
        self.upper_stylization_image_path = 'assets/examples/golden-gate-example.jpg'
        pixmap = QPixmap(self.upper_stylization_image_path)
        upper_stylization_image.setPixmap(pixmap)
        upper_stylization_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        upper_stylization_image.setFixedSize(pixmap.size())
        upper_stylization_image.setObjectName('upper_stylization_image')
        upper_stylization_container_layout.addWidget(upper_stylization_image)

        # lower stylization buttons container
        lower_stylization_buttons_open_file_button = StyleButton('Open File', 'assets/icons/document.png',
                                                                 'lower_open_button')
        lower_stylization_buttons_select_button = StyleButton("Select From Library", 'assets/icons/bookmark.png',
                                                              'lower_library_button')
        lower_stylization_buttons_wikiart_button = StyleButton("Random WikiArt Image", 'assets/icons/shuffle.png',
                                                               'lower_wikiart_button')
        lower_stylization_buttons_layout = QVBoxLayout()
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_open_file_button)
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_select_button)
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_wikiart_button)
        lower_stylization_buttons_layout.addStretch()
        lower_stylization_buttons_container.setLayout(lower_stylization_buttons_layout)

        # lower stylization image container
        lower_stylization_image = QLabel()
        # image = cv.imread('assets/examples/towers-example.jpg')
        # image.resize(256, 256)
        # lower_stylization_image.setPixmap(QPixmap.fromImage(QImage(image, image.shape[0], image.shape[1],
        #                                                            QImage.Format.Format_BGR888)))
        self.lower_stylization_image_path = 'assets/examples/towers-example.jpg'
        pixmap = QPixmap(self.lower_stylization_image_path)
        lower_stylization_image.setPixmap(pixmap)
        lower_stylization_image.setObjectName('lower_stylization_image')
        lower_stylization_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lower_stylization_image.setFixedSize(pixmap.size())
        lower_stylization_container_layout.addWidget(lower_stylization_image)

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

        stylize_button = QPushButton('Stylize')
        icon = QIcon(QPixmap('assets/icons/shuffle.png'))
        stylize_button.setIcon(icon)
        stylize_button.clicked.connect(self.stylize_button_click)
        stylization_controls_container_layout.addWidget(stylize_button)

        # result_image_container
        result_image_container_layout = QVBoxLayout()
        self.result_image = QLabel()
        # result_image.setBaseSize(500, 500)
        # image = cv.imread('assets/examples/style-transfer-result-example.png')
        # image.resize(500, 500)
        # result_image.setPixmap(QPixmap.fromImage(QImage(image, image.shape[0], image.shape[1],
        #                                                 QImage.Format.Format_BGR888)))
        self.result_image.setPixmap(QPixmap('assets/examples/style-transfer-result-example.png'))
        result_image_container_layout.addWidget(self.result_image)
        result_image_container.setLayout(result_image_container_layout)

        # result_controls_container
        result_controls_layout = QGridLayout()
        result_save_library_button = StyleButton('Save To Library', 'assets/icons/book.png')
        result_controls_layout.addWidget(result_save_library_button, 0, 1)
        result_controls_layout.setColumnStretch(0, 1)
        result_controls_layout.setRowStretch(1, 1)
        result_controls_container.setLayout(result_controls_layout)

    def stylize_button_click(self):
        content_image_path = self.upper_stylization_image_path
        style_image_path = self.lower_stylization_image_path
        content_image = preprocess_image(load_img(content_image_path), 384)
        style_image = preprocess_image(load_img(style_image_path), 256)

        content_blending_ratio = (100 - self.stylization_slider.value()) / 100  # define content blending ratio between [0..1].

        # Calculate style bottleneck for the preprocessed style image.
        style_bottleneck = StyleTransfer.run_style_predict(style_image)
        style_bottleneck_content = StyleTransfer.run_style_predict(preprocess_image(content_image, 256))
        style_bottleneck_blended = content_blending_ratio * style_bottleneck_content + (1 - content_blending_ratio) * style_bottleneck

        # Stylize the content image using the style bottleneck.
        result_image = StyleTransfer.run_style_transform(style_bottleneck_blended, content_image)[0]
        from PIL import Image
        # TODO increment counter in this path
        result_path = "assets/examples/result0.png"
        tf.keras.utils.save_img(result_path, result_image)
        self.result_image.setPixmap(QPixmap(result_path))


class RightMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.right_menu_layout = QVBoxLayout()
        self.setLayout(self.right_menu_layout)

        self.right_menu_layout.addWidget(QLabel('Recent artworks'))
        for i in range(5):
            button = QPushButton()
            button.setIcon(QIcon(f'assets/examples/recent-example-{i + 1}.png'))
            button.setIconSize(QSize(120, 120))
            button.setMaximumSize(200, 200)
            self.right_menu_layout.addWidget(button)

        self.right_menu_layout.addStretch()


class StyleButton(QPushButton):

    def __init__(self, label, image_path, button_name: str = ''):
        super().__init__()

        icon = QIcon(QPixmap(image_path))
        self.setIcon(icon)
        self.setText(label)
        self.setStyleSheet('text-align: left; padding: 5px')
        self.setObjectName(button_name)
        self.clicked.connect(self.button_click)

    def button_click(self):
        button = self.sender()
        button_name = button.objectName()

        def open_image_from_file(label_name):
            file = QFileDialog.getOpenFileName(self, 'Select an image', '.', 'Images (*.png *.jpg)')
            if file:
                from main import MainWindow
                window = MainWindow.window(self)
                style_menu: StyleMenu = window.style_menu
                image = style_menu.findChild(QLabel, label_name)
                if file[0] == '':
                    return
                pixmap = QPixmap(file[0])
                if label_name == 'upper_stylization_image':
                    style_menu.upper_stylization_image_path = file[0]
                if label_name == 'lower_stylization_image':
                    style_menu.lower_stylization_image_path = file[0]

                scaled_pixmap = pixmap.scaled(image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                image.setPixmap(scaled_pixmap)

        if button_name == 'upper_open_button':
            open_image_from_file('upper_stylization_image')

        if button_name == 'lower_open_button':
            open_image_from_file('lower_stylization_image')

import cv2
import numpy as np
from PIL.Image import Image
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QFileDialog, QToolTip

from logic.morphing import morphing_handler


class MorphingMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.morphing_layout = QHBoxLayout()
        self.setLayout(self.morphing_layout)

        self.left_container = LeftContainer()
        self.middle_container = MiddleContainer()
        self.right_container = RightContainer()
        self.recent_artwork_container = RecentArtworkMenu()

        self.morphing_layout.addWidget(self.left_container, 2)
        self.morphing_layout.addWidget(self.middle_container, 5)
        self.morphing_layout.addWidget(self.right_container, 2)
        # self.morphing_layout.addWidget(self.recent_artwork_container)

        self.model_trained = False


class LeftContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.setStyleSheet('border: 1px solid red')

        # image
        self.image_container = QWidget()
        self.image_container_layout = QHBoxLayout()
        self.image_container.setLayout(self.image_container_layout)
        self.image_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_container)

        self.image = QLabel()
        self.image_path = 'assets/examples/morphing-example-left.jpg'
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(self.image.size() * 0.6, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image.setPixmap(scaled_pixmap)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setObjectName('morphing_left_image')
        self.image_container_layout.addWidget(self.image)

        # buttons
        self.button_container = QWidget()
        self.button_container_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_container_layout)
        self.layout.addWidget(self.button_container)

        self.left_open_button = MorphingButton('Open file', 'assets/icons/document.png', 'left_open_button')
        self.left_library_button = MorphingButton('Select from library', 'assets/icons/bookmark.png')
        self.button_container_layout.addWidget(self.left_open_button)
        self.button_container_layout.addWidget(self.left_library_button)


class MiddleContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setStyleSheet('border: 1px solid lime')

        # image
        self.image_container = QWidget()
        self.image_container_layout = QHBoxLayout()
        self.image_container.setLayout(self.image_container_layout)
        self.image_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_container)

        self.image = QLabel()
        self.image_path = 'assets/examples/morphing-example-result.jpg'
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(self.image.size() * 0.8, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image.setPixmap(scaled_pixmap)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setObjectName('morphing_result')
        self.image_container_layout.addWidget(self.image)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider.setValue(36)
        self.slider.setMinimum(0)
        self.slider.setMaximum(49)
        self.slider.setSingleStep(1)
        self.slider.setObjectName('morphing_slider')
        self.slider.valueChanged.connect(self.handle_slider_value_change)
        # slider is disabled till model is trained
        self.slider.setEnabled(False)
        self.layout.addWidget(self.slider)

        # buttons
        self.button_container = QWidget()
        self.button_container_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_container_layout)
        self.layout.addWidget(self.button_container)

        self.save_button = MorphingButton('Save to library', 'assets/icons/bookmark.png')
        # button disabled until model is trained
        self.save_button.setEnabled(False)
        self.button_container_layout.addWidget(self.save_button)

        self.train_model_button = MorphingButton('Train model', 'assets/icons/rocket.png', 'button_train_model')
        self.button_container_layout.addWidget(self.train_model_button)
        self.button_container_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

    def handle_slider_value_change(self):
        from main import MainWindow
        window = MainWindow.window(self)

        morphing_menu = window.morphing_menu

        position = self.slider.value()

        morphed_image = morphing_menu.frames[position] \
            if position < len(morphing_menu.frames) else morphing_menu.frames[0]
        morphed_image_path = f'assets/results/morphing_{position}.jpg'

        morphed_image = cv2.cvtColor(morphed_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(morphed_image_path, morphed_image)

        pixmap = QPixmap(morphed_image_path)
        scaled_pixmap = pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image.setPixmap(scaled_pixmap)


class RightContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.setStyleSheet('border: 1px solid blue')

        # image
        self.image_container = QWidget()
        self.image_container_layout = QHBoxLayout()
        self.image_container.setLayout(self.image_container_layout)
        self.image_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_container)

        self.image = QLabel()
        self.image_path = 'assets/examples/morphing-example-right.jpg'
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(self.image.size() * 0.6, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image.setPixmap(scaled_pixmap)
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setObjectName('morphing_right_image')
        self.image_container_layout.addWidget(self.image)

        # buttons
        self.button_container = QWidget()
        self.button_container_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_container_layout)
        self.layout.addWidget(self.button_container)

        self.open_button = MorphingButton('Open file', 'assets/icons/document.png', 'right_open_button')
        self.library_button = MorphingButton('Select from library', 'assets/icons/bookmark.png')
        self.button_container_layout.addWidget(self.open_button)
        self.button_container_layout.addWidget(self.library_button)


class RecentArtworkMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel('Recent artworks'))
        for i in range(5):
            button = QPushButton()
            button.setIcon(QIcon(f'assets/examples/recent-example-{i + 1}.png'))
            button.setIconSize(QSize(120, 120))
            button.setMaximumSize(200, 200)
            self.layout.addWidget(button)

        self.layout.addStretch()


class MorphingButton(QPushButton):

    def __init__(self, label: str, image_path: str, button_name: str = ''):
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

        def open_image_from_file(button_name):
            file = QFileDialog.getOpenFileName(self, 'Select an image', '.', 'Images (*.png *.jpg)')
            if file:
                from main import MainWindow
                window = MainWindow.window(self)
                morphing_menu = window.morphing_menu
                if file[0] == '':
                    return

                image = None
                if button_name == 'left_open_button':
                    morphing_menu.left_container.image_path = file[0]
                    image = morphing_menu.left_container.findChild(QLabel, 'morphing_left_image')
                if button_name == 'right_open_button':
                    morphing_menu.right_container.image_path = file[0]
                    image = morphing_menu.right_container.findChild(QLabel, 'morphing_right_image')

                if not image:
                    return

                pixmap = QPixmap(file[0])
                scaled_pixmap = pixmap.scaled(image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                image.setPixmap(scaled_pixmap)

                morphing_menu.model_trained = False
                morphing_menu.middle_container.slider.setEnabled(False)
                morphing_menu.middle_container.save_button.setEnabled(False)

        if button_name == 'left_open_button' or button_name == 'right_open_button':
            open_image_from_file(button_name)

        if button_name == 'button_train_model':
            from main import MainWindow
            window = MainWindow.window(self)
            morphing_menu = window.morphing_menu

            morphing_menu.frames = morphing_handler(
                image_left_path=morphing_menu.left_container.image_path,
                image_right_path=morphing_menu.right_container.image_path)

            morphing_menu.model_trained = True
            morphing_menu.middle_container.slider.setEnabled(True)
            morphing_menu.middle_container.save_button.setEnabled(True)

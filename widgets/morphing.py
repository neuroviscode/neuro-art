import copy
import os

import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QProgressBar, QFileDialog

from logic import morphing


class MorphingMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.morphing_layout = QHBoxLayout()
        self.setLayout(self.morphing_layout)

        self.left_container = LeftContainer()
        self.middle_container = MiddleContainer()
        self.right_container = RightContainer()

        self.morphing_layout.addWidget(self.left_container, 2)
        self.morphing_layout.addWidget(self.middle_container, 5)
        self.morphing_layout.addWidget(self.right_container, 2)

        self.frames = []


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
        self.image_path = os.path.abspath('assets/examples/morphing_example_1.jpg')
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

        self.left_open_button = MorphingButton('Open file', 'assets/icons/document.png',
                                               callback=self.open_image_picker)
        self.left_library_button = MorphingButton('Select from library', 'assets/icons/bookmark.png')
        self.button_container_layout.addWidget(self.left_open_button)
        self.button_container_layout.addWidget(self.left_library_button)

    def open_image_picker(self) -> None:
        file = QFileDialog.getOpenFileName(self, 'Select an image', '.', 'Images (*.png *.jpg)')
        if file:
            if file[0] == '':
                return
            pixmap = QPixmap(file[0])
            self.image_path = file[0]
            scaled_pixmap = pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.image.setPixmap(scaled_pixmap)


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
        self.layout.addWidget(self.slider)

        # progress bar
        self.progress_bar_container = QWidget()
        self.progress_bar_container_layout = QVBoxLayout()
        self.progress_bar_container.setLayout(self.progress_bar_container_layout)
        self.layout.addWidget(self.progress_bar_container)

        self.training_label = QLabel('Training progress')
        self.training_label.setStyleSheet('padding-top: 20px')
        self.progress_bar_container_layout.addWidget(self.training_label)
        self.morphing_train_progress_bar = QProgressBar()
        self.morphing_train_progress_bar.setRange(0, 100)
        self.progress_bar_container_layout.addWidget(self.morphing_train_progress_bar)

        self.progress_bar_container_layout.addWidget(QLabel('Morphing progress'))
        self.morphing_morph_progress_bar = QProgressBar()
        self.morphing_morph_progress_bar.setRange(0, 100)
        self.progress_bar_container_layout.addWidget(self.morphing_morph_progress_bar)

        # buttons
        self.button_container = QWidget()
        self.button_container_layout = QHBoxLayout()
        self.button_container.setLayout(self.button_container_layout)
        self.button_container_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.train_button = MorphingButton(
            'Train model',
            'assets/icons/refresh.png',
            callback=self.start_morphing_training
        )
        self.button_container_layout.addWidget(self.train_button)
        self.layout.addWidget(self.button_container)
        self.save_button = MorphingButton('Save to library', 'assets/icons/bookmark.png')
        self.button_container_layout.addWidget(self.save_button)
        self.slider.setDisabled(True)

    def handle_slider_value_change(self):
        from widgets.main_window import MainWindow
        window = MainWindow.window(self)

        morphing_menu = window.morphing_menu

        position = self.slider.value()

        morphed_image = morphing_menu.frames[position]
        morphed_image_path = f'assets/results/morphing/morphing_{position}.jpg'

        morphed_image = cv2.cvtColor(morphed_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(morphed_image_path, morphed_image)

        pixmap = QPixmap(morphed_image_path)
        scaled_pixmap = pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image.setPixmap(scaled_pixmap)

    def start_morphing_training(self):
        self.save_button.setDisabled(True)
        self.train_button.setDisabled(True)

        from widgets.main_window import MainWindow
        window = MainWindow.window(self)
        left_path = window.morphing_menu.left_container.image_path
        right_path = window.morphing_menu.right_container.image_path

        self.morphing_thread = QThread()
        self.morphing_worker = MorphingWorker(morphing.morphing_handler, left_path, right_path)
        self.morphing_worker.moveToThread(self.morphing_thread)

        self.morphing_train_progress_bar.setValue(0)
        self.morphing_morph_progress_bar.setValue(0)

        self.morphing_thread.started.connect(self.morphing_worker.run)
        self.morphing_worker.finished.connect(self.morphing_thread.quit)
        self.morphing_worker.finished.connect(self.morphing_thread.deleteLater)
        self.morphing_worker.finished.connect(self.morphing_training_finished)

        self.morphing_worker.training_progress.connect(self.update_training_progress_bar)
        self.morphing_worker.morphing_progress.connect(self.update_morphing_progress_bar)

        self.morphing_thread.start()

    def morphing_training_finished(self, frames: list):
        from widgets.main_window import MainWindow
        window = MainWindow.window(self)
        morphing_menu = window.morphing_menu

        morphing_menu.frames = copy.deepcopy(frames)

        self.handle_slider_value_change()

        self.save_button.setDisabled(False)
        self.train_button.setDisabled(False)
        self.slider.setDisabled(False)

    def update_training_progress_bar(self, value: int) -> None:
        """
        Updates morphing train progress bar to the passed value

        Parameters
        ----------
        value: int
            Value between 1 and 100 to set the progress bar to
        """
        if value < 0 or value > 100:
            raise ValueError('Progress bar value must be between <0, 100>')

        self.morphing_train_progress_bar.setValue(value)

    def update_morphing_progress_bar(self, value: int) -> None:
        """
        Updates morphing train progress bar to the passed value

        Parameters
        ----------
        value: int
            Value between 1 and 100 to set the progress bar to
        """
        if value < 0 or value > 100:
            raise ValueError('Progress bar value must be between <0, 100>')

        self.morphing_morph_progress_bar.setValue(value)


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
        self.image_path = os.path.abspath('assets/examples/morphing_example_2.jpg')
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

        self.open_button = MorphingButton(
            'Open file',
            'assets/icons/document.png',
            callback=self.open_image_picker)
        self.library_button = MorphingButton('Select from library', 'assets/icons/bookmark.png')
        self.button_container_layout.addWidget(self.open_button)
        self.button_container_layout.addWidget(self.library_button)

    def open_image_picker(self) -> None:
        file = QFileDialog.getOpenFileName(self, 'Select an image', '.', 'Images (*.png *.jpg)')
        if file:
            if file[0] == '':
                return
            pixmap = QPixmap(file[0])
            self.image_path = file[0]
            scaled_pixmap = pixmap.scaled(self.image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.image.setPixmap(scaled_pixmap)


class MorphingButton(QPushButton):

    def __init__(self, label: str, image_path: str, button_name: str = '', callback=None):
        super().__init__()

        icon = QIcon(QPixmap(image_path))
        self.setIcon(icon)
        self.setText(label)
        self.setStyleSheet('text-align: left; padding: 5px')
        self.setObjectName(button_name)
        if callback:
            self.clicked.connect(callback)


class MorphingWorker(QObject):
    """Class defining worker used for morphing process in a separate thread"""
    finished = pyqtSignal(list)
    training_progress = pyqtSignal(int)
    morphing_progress = pyqtSignal(int)

    def __init__(self, morphing_callback, right_path, left_path, *args, **kwargs):
        super().__init__()
        self.morphing_callback = morphing_callback
        self.args = args
        self.kwargs = kwargs
        self.right_path = right_path
        self.left_path = left_path

    def run(self):
        result = self.morphing_callback(
            *self.args, **self.kwargs,
            src_path_1=self.right_path,
            src_path_2=self.left_path,
            training_signal=self.training_progress,
            morphing_signal=self.morphing_progress)

        self.finished.emit(result)

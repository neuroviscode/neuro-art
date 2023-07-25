from PyQt6.QtCore import Qt, QUrl, QObject, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSlider, QFileDialog, \
    QStyle, QProgressBar

from logic.style_transfer import StyleTransfer


class StyleVideoMenu(QWidget):
    """Class defining GUI for video style transfer module"""
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
        upper_stylization_video_container = QWidget()
        upper_stylization_container_layout = QHBoxLayout()
        upper_stylization_container_layout.addWidget(upper_stylization_buttons_container)
        upper_stylization_container_layout.addWidget(upper_stylization_video_container)
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
                                                                 callback=self.open_video_from_file)
        upper_stylization_buttons_select_button = StyleButton(label='Select From Library',
                                                              icon_image_path='assets/icons/bookmark.png',
                                                              button_name='upper_library_button')
        upper_stylization_buttons_layout = QVBoxLayout()
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_open_file_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_select_button)
        upper_stylization_buttons_layout.addStretch()
        upper_stylization_buttons_container.setLayout(upper_stylization_buttons_layout)

        upper_stylization_video_container_layout = QVBoxLayout()
        self.upper_stylization_media_player = QMediaPlayer()
        self.upper_stylization_video_path = "assets/examples/horse.mp4"
        self.upper_stylization_media_player.setSource(QUrl(self.upper_stylization_video_path))
        self.upper_stylization_video = QVideoWidget()
        self.upper_stylization_media_player.setVideoOutput(self.upper_stylization_video)
        self.upper_stylization_video.setObjectName('upper_stylization_video')
        self.upper_stylization_media_player.play()  # without playing and pausing the video were not visible
        self.upper_stylization_media_player.pause()
        self.upper_stylization_media_player.setPosition(0)
        upper_stylization_video_container_layout.addWidget(self.upper_stylization_video)
        upper_stylization_video_container.setLayout(upper_stylization_video_container_layout)

        # lower stylization buttons container
        lower_stylization_buttons_open_file_button = StyleButton(label='Open File',
                                                                 icon_image_path='assets/icons/document.png',
                                                                 button_name='lower_open_button',
                                                                 callback=self.open_image_from_file)
        lower_stylization_buttons_select_button = StyleButton(label='Select From Library',
                                                              icon_image_path='assets/icons/bookmark.png',
                                                              button_name='lower_library_button')
        lower_stylization_buttons_wikiart_button = StyleButton(label='Random WikiArt Image',
                                                               icon_image_path='assets/icons/shuffle.png',
                                                               button_name='lower_wikiart_button')
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
        result_video_container = QWidget()
        result_controls_container = QWidget()
        right_container_layout.addWidget(stylization_controls_container)
        right_container_layout.addWidget(result_video_container)
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

        self.stylize_button = QPushButton('Stylize')
        icon = QIcon(QPixmap('assets/icons/shuffle.png'))
        self.stylize_button.setIcon(icon)
        self.stylize_button.clicked.connect(self.stylize_button_click)
        stylization_controls_container_layout.addWidget(self.stylize_button)

        # result_video_container
        result_video_container_layout = QVBoxLayout()
        self.result_media_player = QMediaPlayer()
        self.result_video_path = "assets/examples/horse.mp4"
        self.result_media_player.setSource(QUrl(self.result_video_path))
        self.result_video = QVideoWidget()
        self.result_media_player.setVideoOutput(self.result_video)
        self.result_media_player.positionChanged.connect(self.video_position_changed)
        self.result_media_player.durationChanged.connect(self.video_duration_changed)
        self.result_media_player.play()  # without playing and pausing the video were not visible
        self.result_media_player.pause()
        self.result_media_player.setPosition(0)
        self.stylization_progress_bar = QProgressBar()
        self.stylization_progress_bar.setRange(0, 100)
        self.video_position_slider = QSlider(Qt.Orientation.Horizontal)
        self.video_position_slider.setRange(0, self.upper_stylization_media_player.duration())
        self.video_position_slider.sliderMoved.connect(self.set_video_position)
        play_button = QPushButton()
        play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        play_button.clicked.connect(self.play_button_click)
        result_video_container_layout.addWidget(self.result_video)
        result_video_container_layout.addWidget(self.stylization_progress_bar)
        result_video_container_layout.addWidget(self.video_position_slider)
        result_video_container_layout.addWidget(play_button)
        result_video_container.setLayout(result_video_container_layout)

        # result_controls_container
        result_controls_layout = QGridLayout()
        result_save_library_button = StyleButton('Save To Library', 'assets/icons/book.png')
        result_controls_layout.addWidget(result_save_library_button, 0, 1)
        result_controls_layout.setColumnStretch(0, 1)
        result_controls_layout.setRowStretch(1, 1)
        result_controls_container.setLayout(result_controls_layout)

    def stylize_button_click(self) -> None:
        """Callback to stylize button, starts stylization process in a separate thread"""
        StyleTransfer.set_mode(StyleTransfer.StyleTransferMode.VIDEO)  # set proper stylization models as active
        self.stylize_button.setDisabled(True)
        self.reset_videos_state()

        style_image_path = self.lower_stylization_image_path
        content_video_path = self.upper_stylization_video_path
        content_blending_ratio = (100 - self.stylization_slider.value()) / 100  # define content blending ratio between [0..1].

        self.stylization_thread = QThread()
        self.stylization_worker = StylizationWorker(StyleTransfer.stylize_video, content_video_path, style_image_path,
                                                    content_blending_ratio)
        self.stylization_worker.moveToThread(self.stylization_thread)
        self.stylization_thread.started.connect(self.stylization_worker.run)
        self.stylization_worker.progress.connect(self.update_progress_bar)
        self.stylization_worker.finished.connect(self.stylization_thread.quit)
        self.stylization_worker.finished.connect(self.stylization_finished)
        self.stylization_worker.finished.connect(self.stylization_worker.deleteLater)
        self.stylization_thread.finished.connect(self.stylization_thread.deleteLater)
        self.stylization_thread.start()

    def play_button_click(self) -> None:
        """Callback to play button"""
        if self.result_media_player.isPlaying():
            self.result_media_player.pause()
            self.upper_stylization_media_player.pause()
        else:
            self.result_media_player.play()
            self.upper_stylization_media_player.play()

    def set_video_position(self, position: int) -> None:
        """Callback to moving slider
        :param position: expressed in milliseconds since the beginning of the media"""
        self.result_media_player.setPosition(position)
        self.upper_stylization_media_player.setPosition(position)

    def video_position_changed(self, position: int) -> None:
        """Callback to video position changed in QMediaPlayer
        :param position: expressed in milliseconds since the beginning of the media"""
        self.video_position_slider.setValue(position)

    def video_duration_changed(self, duration: int) -> None:
        """Callback to video duration changed in QMediaPlayer
        :param duration: total playback time in milliseconds"""
        self.video_position_slider.setRange(0, duration)

    def update_progress_bar(self, value: int) -> None:
        """Callback to stylization progress signal
        :param value: value between 0 and 100"""
        self.stylization_progress_bar.setValue(value)

    def stylization_finished(self, result_video_path: str) -> None:
        """Callback to stylization finished signal, handles setting proper videos in widgets
        :param result_video_path: path of the stylized video"""
        self.result_video_path = result_video_path
        self.reset_videos_state()

        self.result_media_player.setSource(QUrl(self.result_video_path))
        self.result_media_player.setVideoOutput(self.result_video)

        self.result_media_player.play()
        self.upper_stylization_media_player.play()
        self.stylize_button.setDisabled(False)

    def reset_videos_state(self) -> None:
        """Reset both of the videos to their starting point"""
        self.result_media_player.pause()
        self.upper_stylization_media_player.pause()
        self.result_media_player.setPosition(0)
        self.upper_stylization_media_player.setPosition(0)
        self.video_position_slider.setValue(0)

    def open_video_from_file(self) -> None:
        """Callback to open button"""
        file = QFileDialog.getOpenFileName(self, 'Select a video', '.', 'Videos (*.mp4 *.avi)')
        if file:
            if file[0] == '':
                return
            self.reset_videos_state()

            self.upper_stylization_video_path = file[0]
            self.upper_stylization_media_player.setSource(QUrl(self.upper_stylization_video_path))
            self.upper_stylization_media_player.setVideoOutput(self.upper_stylization_video)
            self.upper_stylization_media_player.play()

    def open_image_from_file(self) -> None:
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


class StylizationWorker(QObject):
    """Class defining worker used for stylization process in a separate thread"""
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, stylizing_function, *args, **kwargs):
        super().__init__()
        self.stylizing_function = stylizing_function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result_path = self.stylizing_function(*self.args, progress_signal=self.progress, **self.kwargs)
        self.finished.emit(result_path)

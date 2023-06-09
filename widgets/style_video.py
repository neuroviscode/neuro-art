from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSlider, QFileDialog, \
    QStyle

from logic.style_transfer import StyleTransfer


class StyleVideoMenu(QWidget):
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
        upper_stylization_buttons_open_file_button = StyleButton('Open File', 'assets/icons/document.png',
                                                                 'upper_open_button')
        upper_stylization_buttons_select_button = StyleButton("Select From Library", 'assets/icons/bookmark.png',
                                                              'upper_library_button')
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
        self.upper_stylization_media_player.play()
        self.upper_stylization_media_player.pause()
        self.upper_stylization_media_player.setPosition(0)
        upper_stylization_video_container_layout.addWidget(self.upper_stylization_video)
        upper_stylization_video_container.setLayout(upper_stylization_video_container_layout)


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

        stylize_button = QPushButton('Stylize')
        icon = QIcon(QPixmap('assets/icons/shuffle.png'))
        stylize_button.setIcon(icon)
        stylize_button.clicked.connect(self.stylize_button_click)
        stylization_controls_container_layout.addWidget(stylize_button)

        # result_video_container
        result_video_container_layout = QVBoxLayout()
        self.result_media_player = QMediaPlayer()
        self.result_video_path = "assets/examples/horse.mp4"
        self.result_media_player.setSource(QUrl(self.result_video_path))
        self.result_video = QVideoWidget()
        self.result_media_player.setVideoOutput(self.result_video)
        self.result_media_player.positionChanged.connect(self.video_position_changed)
        self.result_media_player.durationChanged.connect(self.video_duration_changed)
        self.result_media_player.play() # without playing and pausing the video were not visible
        self.result_media_player.pause()
        self.result_media_player.setPosition(0)
        self.video_position_slider = QSlider(Qt.Orientation.Horizontal)
        self.video_position_slider.setRange(0, self.upper_stylization_media_player.duration())
        self.video_position_slider.sliderMoved.connect(self.set_video_position)
        play_button = QPushButton()
        play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        play_button.clicked.connect(self.play_button_click)
        result_video_container_layout.addWidget(self.result_video)
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

    def stylize_button_click(self):
        self.result_media_player.pause()
        self.upper_stylization_media_player.pause()
        self.result_media_player.setPosition(0)
        self.upper_stylization_media_player.setPosition(0)
        self.video_position_slider.setValue(0)

        style_image_path = self.lower_stylization_image_path
        content_video_path = self.upper_stylization_video_path
        content_blending_ratio = (100 - self.stylization_slider.value()) / 100  # define content blending ratio between [0..1].

        self.result_video_path = StyleTransfer.stylize_video(content_video_path, style_image_path, content_blending_ratio)

        self.result_media_player.setSource(QUrl(self.result_video_path))
        self.result_media_player.setVideoOutput(self.result_video)

        self.result_media_player.play()
        self.upper_stylization_media_player.play()

    def play_button_click(self):
        if self.result_media_player.isPlaying():
            self.result_media_player.pause()
            self.upper_stylization_media_player.pause()
        else:
            self.result_media_player.play()
            self.upper_stylization_media_player.play()

    def set_video_position(self, position):
        self.result_media_player.setPosition(position)
        self.upper_stylization_media_player.setPosition(position)

    def video_position_changed(self, position):
        self.video_position_slider.setValue(position)

    def video_duration_changed(self, duration):
        self.video_position_slider.setRange(0, duration)


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

        def open_video_from_file():
            file = QFileDialog.getOpenFileName(self, 'Select a video', '.', 'Videos (*.mp4)')
            if file:
                from main import MainWindow
                window = MainWindow.window(self)
                style_menu: StyleVideoMenu = window.style_video_menu
                if file[0] == '':
                    return
                style_menu.result_media_player.pause()
                style_menu.upper_stylization_media_player.pause()

                style_menu.upper_stylization_video_path = file[0]
                style_menu.upper_stylization_media_player.setSource(QUrl(style_menu.upper_stylization_video_path))
                style_menu.upper_stylization_media_player.setVideoOutput(style_menu.upper_stylization_video)
                style_menu.upper_stylization_media_player.play()

        def open_image_from_file():
            file = QFileDialog.getOpenFileName(self, 'Select an image', '.', 'Images (*.png *.jpg)')
            if file:
                from main import MainWindow
                window = MainWindow.window(self)
                style_menu: StyleVideoMenu = window.style_video_menu
                image = style_menu.findChild(QLabel, 'lower_stylization_image')
                if file[0] == '':
                    return
                pixmap = QPixmap(file[0])
                style_menu.lower_stylization_image_path = file[0]

                scaled_pixmap = pixmap.scaled(image.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                image.setPixmap(scaled_pixmap)

        if button_name == 'upper_open_button':
            open_video_from_file()

        if button_name == 'lower_open_button':
            open_image_from_file()

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSlider


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
        upper_stylization_buttons_open_file_button = StyleButton('Open File', 'assets/icons/document.png')
        upper_stylization_buttons_select_button = StyleButton("Select From Library", 'assets/icons/bookmark.png')
        upper_stylization_buttons_wikiart_button = StyleButton("Random WikiArt Image", 'assets/icons/shuffle.png')
        upper_stylization_buttons_layout = QVBoxLayout()
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_open_file_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_select_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_wikiart_button)
        upper_stylization_buttons_layout.addStretch()
        upper_stylization_buttons_container.setLayout(upper_stylization_buttons_layout)

        # upper stylization image container
        upper_stylization_image = QLabel()
        upper_stylization_image.setPixmap(QPixmap('assets/examples/golden-gate-example.jpg'))
        upper_stylization_container_layout.addWidget(upper_stylization_image)

        # lower stylization buttons container
        lower_stylization_buttons_open_file_button = StyleButton('Open File', 'assets/icons/document.png')
        lower_stylization_buttons_select_button = StyleButton("Select From Library", 'assets/icons/bookmark.png')
        lower_stylization_buttons_wikiart_button = StyleButton("Random WikiArt Image", 'assets/icons/shuffle.png')
        lower_stylization_buttons_layout = QVBoxLayout()
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_open_file_button)
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_select_button)
        lower_stylization_buttons_layout.addWidget(lower_stylization_buttons_wikiart_button)
        lower_stylization_buttons_layout.addStretch()
        lower_stylization_buttons_container.setLayout(lower_stylization_buttons_layout)

        # lower stylization image container
        lower_stylization_image = QLabel()
        lower_stylization_image.setPixmap(QPixmap('assets/examples/towers-example.jpg'))
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

        self.stylization_slider.valueChanged.connect(self.slider_demo)

        stylize_button = QPushButton('Stylize')
        icon = QIcon(QPixmap('assets/icons/shuffle.png'))
        stylize_button.setIcon(icon)
        stylization_controls_container_layout.addWidget(stylize_button)

        # result_image_container
        result_image_container.setMinimumSize(400, 400)
        result_image_container_layout = QVBoxLayout()
        result_image = QLabel()
        result_image.setPixmap(QPixmap('assets/examples/style-transfer-result-example.png'))
        result_image_container_layout.addWidget(result_image)
        result_image_container.setLayout(result_image_container_layout)

        # result_controls_container
        result_controls_layout = QGridLayout()
        result_save_library_button = StyleButton('Save To Library', 'assets/icons/book.png')
        result_controls_layout.addWidget(result_save_library_button, 0, 1)
        result_controls_layout.setColumnStretch(0, 1)
        result_controls_layout.setRowStretch(1, 1)
        result_controls_container.setLayout(result_controls_layout)

    def slider_demo(self):
        print(self.stylization_slider.value())


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

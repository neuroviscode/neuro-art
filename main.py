import sys

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QPixmap, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel, \
    QSpacerItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("neuroART")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(960, 560))

        self.main_window_layout = QHBoxLayout()

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_window_layout)
        self.setCentralWidget(self.central_widget)

        self.main_window_layout.addWidget(LeftMenu())
        # TODO home menu
        # self.main_window_layout.addWidget(MainMenu())
        self.main_window_layout.addWidget(StyleTransferMenu())
        self.main_window_layout.addWidget(RightMenu())

        # -- Menu bar --
        menu_bar = self.menuBar()
        menu_bar.setCornerWidget(QLabel('NeuroART'), Qt.Corner.TopLeftCorner)
        menu_bar.setMinimumSize(400, 30)

        file_menu = menu_bar.addMenu('File')
        open_action = QAction('Open', self)
        close_action = QAction('Exit', self)
        file_menu.addAction(open_action)
        file_menu.addAction(close_action)

        edit_menu = menu_bar.addMenu('Edit')
        undo_action = QAction('Undo', self)
        redo_action = QAction('Redo', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        help_menu = menu_bar.addMenu('Help')

        self.central_widget.setStyleSheet('border: 1px solid red') # TODO testing purposes, remove later


class LeftMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.left_menu_layout = QVBoxLayout()
        self.setLayout(self.left_menu_layout)

        self.left_menu_layout.addWidget(MenuButton("Home", "assets/icon.png"))
        self.left_menu_layout.addWidget(MenuButton("Generate", "assets/icon.png"))
        self.left_menu_layout.addWidget(MenuButton("Style Transfer", "assets/icon.png"))
        self.left_menu_layout.addWidget(MenuButton("Morphing", "assets/icon.png"))
        self.left_menu_layout.addWidget(MenuButton("Library", "assets/icon.png"))
        self.left_menu_layout.addWidget(MenuButton("Settings", "assets/icon.png"))

        self.left_menu_layout.addStretch()


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.main_menu_layout = QVBoxLayout()
        self.setLayout(self.main_menu_layout)

        self.main_menu_layout.addWidget(QPushButton('test main menu 1'))
        self.main_menu_layout.addWidget(QPushButton('test main menu 2'))


class RightMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.right_menu_layout = QVBoxLayout()
        self.setLayout(self.right_menu_layout)

        self.right_menu_layout.addWidget(QLabel('Recent artworks'))
        self.right_menu_layout.addWidget(QPushButton('test left menu 2'))
        self.right_menu_layout.addWidget(QPushButton('test left menu 3'))

        self.right_menu_layout.addStretch()


class MenuButton(QPushButton):
    def __init__(self, label, image_path):
        super().__init__()

        icon = QIcon(QPixmap(image_path))
        self.setIcon(icon)
        self.setText(label)
        self.setStyleSheet('text-align: left')


class StyleTransferMenu(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        left_container = QWidget()
        right_container = QWidget()
        left_container.setStyleSheet('border: 1px solid blue')
        right_container.setStyleSheet('border: 1px solid green')
        layout.addWidget(left_container)
        layout.addWidget(right_container)

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
        upper_stylization_container.setLayout(upper_stylization_container_layout)

        # lower stylization container
        lower_stylization_buttons_container = QWidget()
        lower_stylization_image_container = QWidget()
        lower_stylization_container_layout = QHBoxLayout()
        lower_stylization_container_layout.addWidget(lower_stylization_buttons_container)
        lower_stylization_container_layout.addWidget(lower_stylization_image_container)
        lower_stylization_container.setLayout(lower_stylization_container_layout)

        # upper stylization buttons container
        upper_stylization_buttons_open_file_button = QPushButton("Open File")
        upper_stylization_buttons_select_button = QPushButton("Select From Library")
        upper_stylization_buttons_wikiart_button = QPushButton("Random WikiArt Image")
        upper_stylization_buttons_layout = QVBoxLayout()
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_open_file_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_select_button)
        upper_stylization_buttons_layout.addWidget(upper_stylization_buttons_wikiart_button)



        # right container
        right_container_layout = QVBoxLayout()
        right_container.setLayout(right_container_layout)
        stylization_controls_container = QWidget()
        result_image_container = QWidget()
        result_controls_container = QWidget()
        right_container_layout.addWidget(stylization_controls_container)
        right_container_layout.addWidget(result_image_container)
        right_container_layout.addWidget(result_controls_container)

        # stylization_controls_container
        stylization_controls_container_layout = QVBoxLayout()
        stylization_controls_container.setLayout(stylization_controls_container_layout)

        stylization_controls_container_layout.addWidget(QLabel('tmp-stylization-strength'))

        stylize_button = QPushButton('Stylize')
        icon = QIcon(QPixmap('assets/icon.png'))
        stylize_button.setIcon(icon)
        stylization_controls_container_layout.addWidget(stylize_button)

        # result_image_container
        result_image_container.setMinimumSize(400, 400)
        result_image_container_layout = QVBoxLayout()
        result_image = QLabel()
        result_image.setPixmap(QPixmap('assets/style-transfer-example.png'))
        result_image_container_layout.addWidget(result_image)
        result_image_container.setLayout(result_image_container_layout)


        # result_controls_container




app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

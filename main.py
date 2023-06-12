import sys

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QLabel, \
    QStackedLayout

from widgets.generate import GenerateMenu
from widgets.home import HomeMenu
from widgets.library import LibraryMenu
from widgets.morphing import MorphingMenu
from widgets.settings import SettingsMenu
from widgets.style import StyleMenu


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # initial configuration
        self.setWindowTitle("neuroART")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(960, 560))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # initialize menus
        self.home_menu = HomeMenu()
        self.style_menu = StyleMenu()
        self.morphing_menu = MorphingMenu()
        self.generate_menu = GenerateMenu()
        self.settings_menu = SettingsMenu()
        self.library_menu = LibraryMenu()

        # main window layout
        self.main_window_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_window_layout)

        # left menu
        self.main_window_layout.addWidget(LeftMenu())

        # stacked layout
        self.stacked_layout = QStackedLayout()
        self.main_window_layout.addLayout(self.stacked_layout)
        self.stacked_layout.addWidget(self.style_menu)
        self.stacked_layout.addWidget(self.home_menu)
        self.stacked_layout.addWidget(self.generate_menu)
        self.stacked_layout.addWidget(self.library_menu)
        self.stacked_layout.addWidget(self.settings_menu)
        self.stacked_layout.addWidget(self.morphing_menu)
        self.stacked_layout.setCurrentWidget(self.style_menu)

        self.stacked_layout.setCurrentWidget(self.style_menu)

        # right menu TODO this should be in the style transfer widget
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

        # self.central_widget.setStyleSheet('border: 1px solid red')  # TODO testing purposes, remove later

    @staticmethod
    def change_current_widget(widget: QWidget):
        window.stacked_layout.setCurrentWidget(widget)


class LeftMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.left_menu_layout = QVBoxLayout()
        self.setLayout(self.left_menu_layout)

        self.left_menu_layout.addWidget(MenuButton("Home", "assets/icons/home.png", button_name='btn_leftmenu_home'))
        self.left_menu_layout.addWidget(
            MenuButton("Generate", "assets/icons/bulb.png", button_name='btn_leftmenu_generate'))
        self.left_menu_layout.addWidget(
            MenuButton("Style Transfer", "assets/icons/shuffle.png", button_name='btn_leftmenu_style'))
        self.left_menu_layout.addWidget(
            MenuButton("Morphing", "assets/icons/color-filter.png", button_name='btn_leftmenu_morphing'))
        self.left_menu_layout.addWidget(
            MenuButton("Library", "assets/icons/book.png", button_name='btn_leftmenu_library'))
        self.left_menu_layout.addWidget(
            MenuButton("Settings", "assets/icons/settings.png", button_name='btn_leftmenu_settings'))

        self.left_menu_layout.addStretch()


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


class MenuButton(QPushButton):

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

        if button_name == 'btn_leftmenu_home':
            print('menu button clicked')
            window.change_current_widget(window.home_menu)

        if button_name == 'btn_leftmenu_style':
            print('style button clicked')
            window.change_current_widget(window.style_menu)

        if button_name == 'btn_leftmenu_generate':
            print('generate button clicked')
            window.change_current_widget(window.generate_menu)

        if button_name == 'btn_leftmenu_library':
            print('library button clicked')
            window.change_current_widget(window.library_menu)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

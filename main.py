from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QPushButton, QStackedLayout

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
        self.resize(1400, 720)
        self.setMinimumSize(QtCore.QSize(1360, 720))
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

        # self.central_widget.setStyleSheet('border: 1px solid red')  # TODO testing purposes, remove later

    def change_current_widget(self, widget: QWidget):
        self.stacked_layout.setCurrentWidget(widget)


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


class MenuButton(QPushButton):

    def __init__(self, label, image_path, button_name: str = ''):
        super().__init__()

        icon = QIcon(QPixmap(image_path))
        self.setIcon(icon)
        self.setText(label)
        self.setStyleSheet('text-align: left; padding: 5px 12px;')
        self.setObjectName(button_name)
        self.clicked.connect(self.button_click)

    def button_click(self):
        button = self.sender()
        button_name = button.objectName()

        window = MainWindow.window(self)
        if button_name == 'btn_leftmenu_home':
            window.change_current_widget(window.home_menu)

        if button_name == 'btn_leftmenu_style':
            window.change_current_widget(window.style_menu)

        if button_name == 'btn_leftmenu_generate':
            window.change_current_widget(window.generate_menu)

        if button_name == 'btn_leftmenu_morphing':
            window.change_current_widget(window.morphing_menu)

        if button_name == 'btn_leftmenu_library':
            window.change_current_widget(window.library_menu)

        if button_name == 'btn_leftmenu_settings':
            window.change_current_widget(window.settings_menu)

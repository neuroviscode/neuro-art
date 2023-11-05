import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
import qdarktheme


class SettingsMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.settings_layout = QVBoxLayout()
        self.setLayout(self.settings_layout)

        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.settings_header = QLabel('Application settings:')
        self.settings_header.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.settings_header.setStyleSheet('font-weight: bold')

        self.themes_layout = QHBoxLayout()
        self.themes = QWidget()
        # self.setStyleSheet('border: 1px solid red')
        self.themes.setLayout(self.themes_layout)
        self.themes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.light_theme_button = QPushButton("LightTheme")
        self.light_theme_button.setIcon(QIcon(QPixmap('assets/icons/sun.png')))
        self.light_theme_button.clicked.connect(self.set_light_theme)

        self.dark_theme_button = QPushButton("DarkTheme")
        self.dark_theme_button.setIcon(QIcon(QPixmap('assets/icons/moon.png')))
        self.dark_theme_button.clicked.connect(self.set_dark_theme)

        self.themes_layout.addWidget(self.light_theme_button)
        self.themes_layout.addWidget(self.dark_theme_button)

        self.epochs_form_layout = QHBoxLayout()
        self.epochs_form = QWidget()
        self.epochs_form.setLayout(self.epochs_form_layout)
        self.epochs_form.setMaximumWidth(300)
        self.epochs_form_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.epochs_val = QLineEdit()
        self.epochs_val.setValidator(QIntValidator())
        self.epochs_val.setMaxLength(3)
        self.epochs_val.setText(os.getenv("TRAIN_EPOCHS"))
        self.epochs_val.textChanged.connect(self.change_epochs)

        self.epochs_form_layout.addWidget(QLabel("Number of morphing training epochs:"))
        self.epochs_form_layout.addWidget(self.epochs_val)

        self.steps_form_layout = QHBoxLayout()
        self.steps_form = QWidget()
        self.steps_form.setLayout(self.steps_form_layout)
        self.steps_form.setMaximumWidth(300)
        self.steps_form_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.steps_val = QLineEdit()
        self.steps_val.setValidator(QIntValidator())
        self.steps_val.setMaxLength(2)
        self.steps_val.setText(os.getenv("MORPHING_STEPS"))
        self.steps_val.textChanged.connect(self.change_steps)

        self.steps_form_layout.addWidget(QLabel("Number of morphing frames:"))
        self.steps_form_layout.addWidget(self.steps_val)


        self.settings_layout.addWidget(self.settings_header)
        self.settings_layout.addWidget(QLabel())
        self.settings_layout.addWidget(self.steps_form)
        self.settings_layout.addWidget(self.epochs_form)
        self.settings_layout.addWidget(self.themes)
        self.set_light_theme()

    def set_light_theme(self):
        qdarktheme.setup_theme("light", custom_colors={"primary": "#111111"}, corner_shape="sharp")

    def set_dark_theme(self):
        qdarktheme.setup_theme("dark", custom_colors={"primary": "#cccccc"}, corner_shape="sharp")

    def change_epochs(self, value):
        try:
            x = max(int(value), 10)
            os.environ["TRAIN_EPOCHS"] = str(x)
        except Exception:
            pass
        finally:
            self.epochs_val.setText(os.getenv("TRAIN_EPOCHS"))

    def change_steps(self, value):
        try:
            x = max(int(value), 3)
            os.environ["MORPHING_STEPS"] = str(x)
        except Exception:
            pass
        finally:
            self.steps_val.setText(os.getenv("MORPHING_STEPS"))

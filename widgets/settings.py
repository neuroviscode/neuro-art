import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QCheckBox
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

        self.interpolation_form_layout = QHBoxLayout()
        self.interpolation_form = QWidget()
        self.interpolation_form.setLayout(self.interpolation_form_layout)
        self.interpolation_form.setMaximumWidth(300)
        self.interpolation_form_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.interpolation_checkbox = QCheckBox()
        self.interpolation_checkbox.setChecked(False)
        self.interpolation_checkbox.stateChanged.connect(self.set_interpolation)
        self.interpolation_val = QLineEdit()
        self.interpolation_val.setValidator(QIntValidator())
        self.interpolation_val.setMaxLength(3)
        self.interpolation_val.setText(os.getenv("INTERPOLATION_STEP"))
        self.interpolation_val.textChanged.connect(self.change_interpolation)
        self.interpolation_val.setDisabled(True)

        self.interpolation_form_layout.addWidget(QLabel("Video interpolation:"))
        self.interpolation_form_layout.addWidget(self.interpolation_checkbox)
        self.interpolation_form_layout.addWidget(QLabel("step:"))
        self.interpolation_form_layout.addWidget(self.interpolation_val)


        self.settings_layout.addWidget(self.settings_header)
        self.settings_layout.addWidget(QLabel())
        self.settings_layout.addWidget(self.epochs_form)
        self.settings_layout.addWidget(self.interpolation_form)
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

    def set_interpolation(self):
        self.interpolation_val.setDisabled(self.interpolation_val.isEnabled())
        os.environ["INTERPOLATION"] = "TRUE" if self.interpolation_val.isEnabled() else "FALSE"

    def change_interpolation(self, value):
        try:
            x = max(int(value), 1)
            os.environ["INTERPOLATION_STEP"] = str(x)
        except Exception:
            pass
        finally:
            self.interpolation_val.setText(os.getenv("INTERPOLATION_STEP"))

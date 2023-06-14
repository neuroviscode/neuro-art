from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SettingsMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.settings_layout = QVBoxLayout()
        self.setLayout(self.settings_layout)

        self.settings_layout.addWidget(QLabel('Welcome in the settings menu'))

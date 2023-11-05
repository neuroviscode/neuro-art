import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
import webbrowser


class HomeMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.home_layout = QVBoxLayout()
        self.home_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.home_layout)

        self.logo = QLabel()
        pixmap = QPixmap(os.path.abspath('assets/icon.png'))
        scaled_pixmap = pixmap.scaled(self.logo.size() * 0.8, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(scaled_pixmap)

        self.link = QLabel('Visit our github! https://github.com/neuroviscode/neuro-art')
        self.link.mousePressEvent = self.open_github
        self.link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.link.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.home_layout.addWidget(self.logo)
        self.home_layout.addWidget(self.link)

    def open_github(self, event):
        webbrowser.open('https://github.com/neuroviscode/neuro-art')
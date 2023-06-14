from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class HomeMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.home_layout = QVBoxLayout()
        self.setLayout(self.home_layout)

        self.home_layout.addWidget(QLabel('Welcome in the home screen'))
        self.home_layout.addWidget(QPushButton('test main menu 1'))
        self.home_layout.addWidget(QPushButton('test main menu 2'))
        self.home_layout.addWidget(QPushButton('test main menu 3'))

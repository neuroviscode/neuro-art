from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class LibraryMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.library_layout = QVBoxLayout()
        self.setLayout(self.library_layout)

        self.library_layout.addWidget(QLabel('Welcome in the library menu'))

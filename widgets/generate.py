from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class GenerateMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.generate_layout = QVBoxLayout()
        self.setLayout(self.generate_layout)

        self.generate_layout.addWidget(QLabel('Welcome in the generation menu'))

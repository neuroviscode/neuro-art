from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MorphingMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.morphing_layout = QVBoxLayout()
        self.setLayout(self.morphing_layout)

        self.morphing_layout.addWidget(QLabel('Welcome in the morphing menu'))

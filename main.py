import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("neuroART")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(960, 560))


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

import sys
import os

from PyQt6.QtWidgets import QApplication
from main import MainWindow


def sync():
    app.sync()


app = QApplication(sys.argv)
os.environ["theme"] = "light"
os.environ["TRAIN_EPOCHS"] = "100"
os.environ["MORPHING_STEPS"] = "50"
window = MainWindow()
window.show()
app.exec()

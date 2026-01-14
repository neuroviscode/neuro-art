import sys
import os

from PyQt6.QtWidgets import QApplication
from widgets.main_window import MainWindow


def sync():
    app.sync()


app = QApplication(sys.argv)
os.environ["theme"] = "light"
os.environ["TRAIN_EPOCHS"] = "100"
os.environ["INTERPOLATION"] = "TRUE"
os.environ["INTERPOLATION_STEP"] = "3"
window = MainWindow()
window.show()
app.exec()

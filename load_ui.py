from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([])

window = uic.loadUi("design_assignment3.ui")
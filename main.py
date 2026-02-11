from window import MainWindow
from PySide6.QtWidgets import *
import sys

#Total Screen
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()




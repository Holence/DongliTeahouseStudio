from dongli_teahouse_studio import PasswordCheckWindow

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from custom_palette import *
import sys

QApplication.setAttribute(Qt.AA_UseOpenGLES)
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication([])
app.setStyle("Fusion")
app.setPalette(MyDarkPalette())
PasswordCheckWindow()
sys.exit(app.exec_())
from dongli_teahouse_studio import DongliTeahouseStudio
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from custom_palette import *
import sys

# QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
# QApplication.setAttribute(Qt.AA_UseOpenGLES)
QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
# QDesktopServices.openUrl(QUrl("https://doc.qt.io/qt-5/qdesktopservices.html", QUrl.TolerantMode));

app = QApplication([])

app.setStyle("Fusion")
app.setPalette(MyDarkPalette())
window=DongliTeahouseStudio()

window.show()
sys.exit(app.exec_())
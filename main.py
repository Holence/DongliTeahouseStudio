import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from custom_palette import *
from dongli_teahouse_studio import *


def login_or_exit(successed):
	chechin.hide()
	if successed==1:
		password=chechin.password
		mainwindow=DongliTeahouseStudio(password)
		mainwindow.quitApp.connect(app.quit)
	else:
		app.quit()
		return

QApplication.setAttribute(Qt.AA_UseOpenGLES)
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication([])
app.setStyle("Fusion")
app.setPalette(MyDarkPalette())

#必须设置这一句！
#如果不设置，当Mainwindow hide之后，在最后一个窗口被关闭的时候（比如老板键之后的重新登入界面点取消，或者关闭Setting界面），程序就会自动quit
#另外如果设置了不自动quit，就得手动app.quit
app.setQuitOnLastWindowClosed(False)

chechin=PasswordCheckWindow()
chechin.closed.connect(login_or_exit)
sys.exit(app.exec_())
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'splash_screen.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        if not SplashScreen.objectName():
            SplashScreen.setObjectName(u"SplashScreen")
        SplashScreen.resize(800, 500)
        icon = QIcon()
        icon.addFile(u":/icon/holoico_trans.ico", QSize(), QIcon.Normal, QIcon.Off)
        SplashScreen.setWindowIcon(icon)
        self.centralwidget = QWidget(SplashScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame {	\n"
"	background-color: rgb(73,17,14);\n"
"	border-radius: 25px;\n"
"}\n"
"\n"
"QLabel{\n"
"	color: rgb(255,213,174);\n"
"}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        self.label_title = QLabel(self.dropShadowFrame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(90, 120, 600, 76))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(40)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_description = QLabel(self.dropShadowFrame)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setGeometry(QRect(90, 200, 600, 31))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(14)
        self.label_description.setFont(font1)
        self.label_description.setStyleSheet(u"")
        self.label_description.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self.dropShadowFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(140, 350, 500, 23))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(8)
        font2.setUnderline(False)
        self.progressBar.setFont(font2)
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"	background-color: rgb(54,0,0);\n"
"	color: rgb(255,213,174);\n"
"	border-style: none;\n"
"	border-radius: 10px;\n"
"	text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"	border-radius: 10px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(234,140,85, 255), stop:1 rgba(204,47,34, 255));\n"
"\n"
"}")
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(24)
        self.label_stastus = QLabel(self.dropShadowFrame)
        self.label_stastus.setObjectName(u"label_stastus")
        self.label_stastus.setGeometry(QRect(90, 380, 600, 21))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(12)
        self.label_stastus.setFont(font3)
        self.label_stastus.setStyleSheet(u"")
        self.label_stastus.setAlignment(Qt.AlignCenter)
        self.label_credits = QLabel(self.dropShadowFrame)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setGeometry(QRect(550, 450, 201, 21))
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(10)
        self.label_credits.setFont(font4)
        self.label_credits.setStyleSheet(u"")
        self.label_credits.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.dropShadowFrame)

        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)

        QMetaObject.connectSlotsByName(SplashScreen)
    # setupUi

    def retranslateUi(self, SplashScreen):
        SplashScreen.setWindowTitle(QCoreApplication.translate("SplashScreen", u"Dongli Teahou Studio", None))
        self.label_title.setText(QCoreApplication.translate("SplashScreen", u"<strong>Dongli Teahouse Studio</strong>", None))
        self.label_description.setText(QCoreApplication.translate("SplashScreen", u"<strong>APP</strong> DESCRIPTION", None))
        self.label_stastus.setText(QCoreApplication.translate("SplashScreen", u"loading...", None))
        self.label_credits.setText(QCoreApplication.translate("SplashScreen", u"<strong>Author</strong>: Holence", None))
    # retranslateUi


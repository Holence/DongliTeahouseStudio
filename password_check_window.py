# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'password_check_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from custom_widget import MyTitleLabel

import resource_rc

class Ui_password_check_window(object):
    def setupUi(self, password_check_window):
        if not password_check_window.objectName():
            password_check_window.setObjectName(u"password_check_window")
        password_check_window.resize(287, 177)
        icon = QIcon()
        icon.addFile(u":/icon/holoico_trans.ico", QSize(), QIcon.Normal, QIcon.Off)
        password_check_window.setWindowIcon(icon)
        password_check_window.setStyleSheet(u"QFrame > QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QFrame > QPushButton:hover{\n"
"	background-color: rgb(40,40,40);\n"
"}\n"
"QFrame > QPushButton:pressed {	\n"
"	background-color: rgb(30,30,30);\n"
"}")
        self.centralwidget = QWidget(password_check_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.title_frame = QFrame(self.centralwidget)
        self.title_frame.setObjectName(u"title_frame")
        self.title_frame.setGeometry(QRect(0, 0, 281, 51))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_frame.sizePolicy().hasHeightForWidth())
        self.title_frame.setSizePolicy(sizePolicy)
        self.title_frame.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.title_frame)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.btn_menu = QPushButton(self.title_frame)
        self.btn_menu.setObjectName(u"btn_menu")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_menu.sizePolicy().hasHeightForWidth())
        self.btn_menu.setSizePolicy(sizePolicy1)
        self.btn_menu.setMinimumSize(QSize(36, 36))
        self.btn_menu.setMaximumSize(QSize(36, 36))
        self.btn_menu.setStyleSheet(u"QPushButton:hover{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.btn_menu.setIcon(icon)
        self.btn_menu.setIconSize(QSize(36, 36))

        self.horizontalLayout.addWidget(self.btn_menu)

        self.label_title_bar_top = MyTitleLabel(self.title_frame)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_title_bar_top.sizePolicy().hasHeightForWidth())
        self.label_title_bar_top.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        font.setStyleStrategy(QFont.PreferDefault)
        self.label_title_bar_top.setFont(font)
        self.label_title_bar_top.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.label_title_bar_top)

        self.btn_close = QPushButton(self.title_frame)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy1.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy1)
        self.btn_close.setMinimumSize(QSize(24, 24))
        self.btn_close.setMaximumSize(QSize(24, 24))
        self.btn_close.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icon/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon1)
        self.btn_close.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.btn_close)

        self.buttonBox = QDialogButtonBox(self.centralwidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(108, 130, 150, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(57, 61, 201, 29))
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(61, 100, 196, 16))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        self.label.setFont(font1)
        self.label.setMargin(0)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 64, 24, 24))
        self.label_2.setPixmap(QPixmap(u":/icon/lock.svg"))
        self.label_2.setScaledContents(False)
        password_check_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(password_check_window)

        QMetaObject.connectSlotsByName(password_check_window)
    # setupUi

    def retranslateUi(self, password_check_window):
        password_check_window.setWindowTitle(QCoreApplication.translate("password_check_window", u"Dongli Teahouse Studio", None))
        self.btn_menu.setText("")
        self.label_title_bar_top.setText(QCoreApplication.translate("password_check_window", u"Dongli Teahouse Studio", None))
        self.btn_close.setText("")
        self.lineEdit.setInputMask("")
        self.lineEdit.setPlaceholderText("")
        self.label.setText("")
        self.label_2.setText("")
    # retranslateUi


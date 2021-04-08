# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_setting_dialog(object):
    def setupUi(self, setting_dialog):
        if not setting_dialog.objectName():
            setting_dialog.setObjectName(u"setting_dialog")
        setting_dialog.resize(562, 346)
        icon = QIcon()
        icon.addFile(u":/icon/holoico.ico", QSize(), QIcon.Normal, QIcon.Off)
        setting_dialog.setWindowIcon(icon)
        self.verticalLayout_5 = QVBoxLayout(setting_dialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_general = QPushButton(setting_dialog)
        self.pushButton_general.setObjectName(u"pushButton_general")
        icon1 = QIcon()
        icon1.addFile(u":/icon/sliders.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_general.setIcon(icon1)
        self.pushButton_general.setIconSize(QSize(32, 32))
        self.pushButton_general.setFlat(True)

        self.verticalLayout_4.addWidget(self.pushButton_general)

        self.pushButton_rss = QPushButton(setting_dialog)
        self.pushButton_rss.setObjectName(u"pushButton_rss")
        icon2 = QIcon()
        icon2.addFile(u":/icon/rss.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_rss.setIcon(icon2)
        self.pushButton_rss.setIconSize(QSize(32, 32))
        self.pushButton_rss.setFlat(True)

        self.verticalLayout_4.addWidget(self.pushButton_rss)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget = QStackedWidget(setting_dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout = QGridLayout(self.page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_file_saving_base = QLineEdit(self.page)
        self.lineEdit_file_saving_base.setObjectName(u"lineEdit_file_saving_base")
        self.lineEdit_file_saving_base.setEnabled(False)

        self.gridLayout.addWidget(self.lineEdit_file_saving_base, 1, 0, 1, 1)

        self.pushButtonfile_saving_base = QPushButton(self.page)
        self.pushButtonfile_saving_base.setObjectName(u"pushButtonfile_saving_base")

        self.gridLayout.addWidget(self.pushButtonfile_saving_base, 1, 1, 1, 1)

        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.lineEdit_font = QLineEdit(self.page)
        self.lineEdit_font.setObjectName(u"lineEdit_font")
        self.lineEdit_font.setEnabled(False)
        self.lineEdit_font.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_font, 3, 0, 1, 1)

        self.pushButton_font = QPushButton(self.page)
        self.pushButton_font.setObjectName(u"pushButton_font")

        self.gridLayout.addWidget(self.pushButton_font, 3, 1, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_2 = QGridLayout(self.page_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_4 = QLabel(self.page_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEdit_pixiv_cookie = QLineEdit(self.page_2)
        self.lineEdit_pixiv_cookie.setObjectName(u"lineEdit_pixiv_cookie")

        self.gridLayout_2.addWidget(self.lineEdit_pixiv_cookie, 0, 1, 1, 1)

        self.lineEdit_instagram_cookie = QLineEdit(self.page_2)
        self.lineEdit_instagram_cookie.setObjectName(u"lineEdit_instagram_cookie")

        self.gridLayout_2.addWidget(self.lineEdit_instagram_cookie, 1, 1, 1, 1)

        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)

        self.checkBox_rss_auto_update = QCheckBox(self.page_2)
        self.checkBox_rss_auto_update.setObjectName(u"checkBox_rss_auto_update")
        self.checkBox_rss_auto_update.setLayoutDirection(Qt.RightToLeft)

        self.gridLayout_2.addWidget(self.checkBox_rss_auto_update, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_3.addWidget(self.stackedWidget)

        self.verticalSpacer = QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(setting_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.retranslateUi(setting_dialog)
        self.buttonBox.accepted.connect(setting_dialog.accept)
        self.buttonBox.rejected.connect(setting_dialog.reject)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(setting_dialog)
    # setupUi

    def retranslateUi(self, setting_dialog):
        setting_dialog.setWindowTitle(QCoreApplication.translate("setting_dialog", u"Setting", None))
        self.pushButton_general.setText("")
        self.pushButton_rss.setText("")
        self.label.setText(QCoreApplication.translate("setting_dialog", u"File Saving Directory", None))
        self.pushButtonfile_saving_base.setText(QCoreApplication.translate("setting_dialog", u"Open...", None))
        self.label_2.setText(QCoreApplication.translate("setting_dialog", u"Font", None))
        self.pushButton_font.setText(QCoreApplication.translate("setting_dialog", u"Font...", None))
        self.label_3.setText(QCoreApplication.translate("setting_dialog", u"Pixiv Cookie\uff08\u4e00\u4e9b\u753b\u5e08\u7684\u9650\u5236\u6bd4\u8f83\u4e25\u683c\uff0c\u9700\u8981cookie\u624d\u80fd\u8bbf\u95ee\u5230\uff09", None))
        self.label_4.setText(QCoreApplication.translate("setting_dialog", u"Instagram Cookie\uff08Instagram\u662f\u4e0d\u5bf9\u5916\u5f00\u653e\u7684\uff09", None))
        self.label_5.setText(QCoreApplication.translate("setting_dialog", u"\u6bcf\u65e5\u81ea\u52a8\u66f4\u65b0", None))
        self.checkBox_rss_auto_update.setText("")
    # retranslateUi


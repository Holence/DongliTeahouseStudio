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
        setting_dialog.resize(433, 237)
        icon = QIcon()
        icon.addFile(u":/icon/holoico.ico", QSize(), QIcon.Normal, QIcon.Off)
        setting_dialog.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(setting_dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(setting_dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.lineEdit_file_saving_base = QLineEdit(setting_dialog)
        self.lineEdit_file_saving_base.setObjectName(u"lineEdit_file_saving_base")
        self.lineEdit_file_saving_base.setEnabled(False)

        self.gridLayout.addWidget(self.lineEdit_file_saving_base, 1, 0, 1, 1)

        self.pushButtonfile_saving_base = QPushButton(setting_dialog)
        self.pushButtonfile_saving_base.setObjectName(u"pushButtonfile_saving_base")

        self.gridLayout.addWidget(self.pushButtonfile_saving_base, 1, 1, 1, 1)

        self.label = QLabel(setting_dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_font = QLineEdit(setting_dialog)
        self.lineEdit_font.setObjectName(u"lineEdit_font")
        self.lineEdit_font.setEnabled(False)
        self.lineEdit_font.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_font, 3, 0, 1, 1)

        self.pushButton_font = QPushButton(setting_dialog)
        self.pushButton_font.setObjectName(u"pushButton_font")

        self.gridLayout.addWidget(self.pushButton_font, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 56, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(setting_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(setting_dialog)
        self.buttonBox.accepted.connect(setting_dialog.accept)
        self.buttonBox.rejected.connect(setting_dialog.reject)

        QMetaObject.connectSlotsByName(setting_dialog)
    # setupUi

    def retranslateUi(self, setting_dialog):
        setting_dialog.setWindowTitle(QCoreApplication.translate("setting_dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("setting_dialog", u"Font", None))
        self.pushButtonfile_saving_base.setText(QCoreApplication.translate("setting_dialog", u"Open...", None))
        self.label.setText(QCoreApplication.translate("setting_dialog", u"File Saving Directory", None))
        self.pushButton_font.setText(QCoreApplication.translate("setting_dialog", u"Font...", None))
    # retranslateUi


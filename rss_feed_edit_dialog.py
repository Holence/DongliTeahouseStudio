# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rss_feed_edit_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_rss_feed_edit_dialog(object):
    def setupUi(self, rss_feed_edit_dialog):
        if not rss_feed_edit_dialog.objectName():
            rss_feed_edit_dialog.setObjectName(u"rss_feed_edit_dialog")
        rss_feed_edit_dialog.resize(636, 454)
        icon = QIcon()
        icon.addFile(u":/icon/holoico.ico", QSize(), QIcon.Normal, QIcon.Off)
        rss_feed_edit_dialog.setWindowIcon(icon)
        self.horizontalLayout_2 = QHBoxLayout(rss_feed_edit_dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listWidget = QListWidget(rss_feed_edit_dialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.horizontalLayout.addWidget(self.listWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(rss_feed_edit_dialog)
        self.label_3.setObjectName(u"label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label_3)

        self.lineEdit_url = QLineEdit(rss_feed_edit_dialog)
        self.lineEdit_url.setObjectName(u"lineEdit_url")
        self.lineEdit_url.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_url)

        self.label_2 = QLabel(rss_feed_edit_dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_name = QLineEdit(rss_feed_edit_dialog)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.verticalLayout.addWidget(self.lineEdit_name)

        self.label = QLabel(rss_feed_edit_dialog)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label)

        self.lineEdit_frequency = QLineEdit(rss_feed_edit_dialog)
        self.lineEdit_frequency.setObjectName(u"lineEdit_frequency")

        self.verticalLayout.addWidget(self.lineEdit_frequency)

        self.label_4 = QLabel(rss_feed_edit_dialog)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.label_4)

        self.lineEdit_unread = QLineEdit(rss_feed_edit_dialog)
        self.lineEdit_unread.setObjectName(u"lineEdit_unread")
        self.lineEdit_unread.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit_unread)

        self.verticalSpacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton = QPushButton(rss_feed_edit_dialog)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(rss_feed_edit_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(rss_feed_edit_dialog)
        self.buttonBox.accepted.connect(rss_feed_edit_dialog.accept)
        self.buttonBox.rejected.connect(rss_feed_edit_dialog.reject)

        QMetaObject.connectSlotsByName(rss_feed_edit_dialog)
    # setupUi

    def retranslateUi(self, rss_feed_edit_dialog):
        rss_feed_edit_dialog.setWindowTitle(QCoreApplication.translate("rss_feed_edit_dialog", u"Edit RSS Feed", None))
        self.label_3.setText(QCoreApplication.translate("rss_feed_edit_dialog", u"Feed Url", None))
        self.label_2.setText(QCoreApplication.translate("rss_feed_edit_dialog", u"Feed Name", None))
        self.label.setText(QCoreApplication.translate("rss_feed_edit_dialog", u"Update Frequency", None))
        self.lineEdit_frequency.setPlaceholderText(QCoreApplication.translate("rss_feed_edit_dialog", u"1,2,3,4,5,6,7", None))
        self.label_4.setText(QCoreApplication.translate("rss_feed_edit_dialog", u"Unread", None))
        self.pushButton.setText(QCoreApplication.translate("rss_feed_edit_dialog", u"Mark All Articles in This Feed", None))
    # retranslateUi


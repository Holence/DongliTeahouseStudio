# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'diary_search_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_diary_search_dialog(object):
    def setupUi(self, diary_search_dialog):
        if not diary_search_dialog.objectName():
            diary_search_dialog.setObjectName(u"diary_search_dialog")
        diary_search_dialog.resize(778, 589)
        icon = QIcon()
        icon.addFile(u":/icon/holoico.ico", QSize(), QIcon.Normal, QIcon.Off)
        diary_search_dialog.setWindowIcon(icon)
        self.verticalLayout_3 = QVBoxLayout(diary_search_dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(diary_search_dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.splitter = QSplitter(diary_search_dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.listWidget = QListWidget(self.splitter)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(220, 0))
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)
        self.listWidget.setSpacing(10)
        self.listWidget.setWordWrap(True)
        self.splitter.addWidget(self.listWidget)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_date = QLineEdit(self.widget)
        self.lineEdit_date.setObjectName(u"lineEdit_date")
        self.lineEdit_date.setEnabled(False)

        self.verticalLayout_2.addWidget(self.lineEdit_date)

        self.listWidget_concept = QListWidget(self.widget)
        self.listWidget_concept.setObjectName(u"listWidget_concept")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_concept.sizePolicy().hasHeightForWidth())
        self.listWidget_concept.setSizePolicy(sizePolicy)
        self.listWidget_concept.setMaximumSize(QSize(16777215, 40))
        self.listWidget_concept.setDragEnabled(False)
        self.listWidget_concept.setDragDropOverwriteMode(False)
        self.listWidget_concept.setDragDropMode(QAbstractItemView.InternalMove)
        self.listWidget_concept.setDefaultDropAction(Qt.MoveAction)
        self.listWidget_concept.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_concept.setMovement(QListView.Free)
        self.listWidget_concept.setFlow(QListView.LeftToRight)
        self.listWidget_concept.setResizeMode(QListView.Adjust)
        self.listWidget_concept.setSpacing(5)
        self.listWidget_concept.setViewMode(QListView.IconMode)
        self.listWidget_concept.setWordWrap(False)
        self.listWidget_concept.setSelectionRectVisible(True)

        self.verticalLayout_2.addWidget(self.listWidget_concept)

        self.textEdit = QTextEdit(self.widget)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy1)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.textEdit)

        self.splitter.addWidget(self.widget)

        self.verticalLayout.addWidget(self.splitter)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.retranslateUi(diary_search_dialog)

        QMetaObject.connectSlotsByName(diary_search_dialog)
    # setupUi

    def retranslateUi(self, diary_search_dialog):
        diary_search_dialog.setWindowTitle(QCoreApplication.translate("diary_search_dialog", u"Search Diary Text", None))
    # retranslateUi


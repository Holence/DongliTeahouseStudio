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
        diary_search_dialog.resize(904, 668)
        icon = QIcon()
        icon.addFile(u":/icon/holoico_trans.ico", QSize(), QIcon.Normal, QIcon.Off)
        diary_search_dialog.setWindowIcon(icon)
        diary_search_dialog.setStyleSheet(u"QListWidget::item:selected {\n"
"    border-radius:5px;\n"
"    background-color:rgb(73, 73, 73);\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(diary_search_dialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.splitter = QSplitter(diary_search_dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.checkBox = QCheckBox(self.layoutWidget)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(self.layoutWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(220, 0))
        self.listWidget.setStyleSheet(u"QListWidget::item {\n"
"    background-color:rgb(51, 51, 51);\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    border-radius:5px;\n"
"    background-color:rgb(73, 73, 73);\n"
"}")
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)
        self.listWidget.setSpacing(10)
        self.listWidget.setWordWrap(True)

        self.verticalLayout.addWidget(self.listWidget)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_date = QLineEdit(self.layoutWidget1)
        self.lineEdit_date.setObjectName(u"lineEdit_date")
        self.lineEdit_date.setEnabled(False)

        self.verticalLayout_2.addWidget(self.lineEdit_date)

        self.listWidget_concept = QListWidget(self.layoutWidget1)
        self.listWidget_concept.setObjectName(u"listWidget_concept")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_concept.sizePolicy().hasHeightForWidth())
        self.listWidget_concept.setSizePolicy(sizePolicy)
        self.listWidget_concept.setMaximumSize(QSize(16777215, 60))
        self.listWidget_concept.setDragEnabled(False)
        self.listWidget_concept.setDragDropOverwriteMode(False)
        self.listWidget_concept.setDragDropMode(QAbstractItemView.NoDragDrop)
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

        self.textEdit = QTextEdit(self.layoutWidget1)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy1)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.textEdit)

        self.splitter.addWidget(self.layoutWidget1)

        self.horizontalLayout_2.addWidget(self.splitter)


        self.retranslateUi(diary_search_dialog)

        QMetaObject.connectSlotsByName(diary_search_dialog)
    # setupUi

    def retranslateUi(self, diary_search_dialog):
        diary_search_dialog.setWindowTitle(QCoreApplication.translate("diary_search_dialog", u"Search Diary Text", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("diary_search_dialog", u"Search Text&Concept Name", None))
        self.checkBox.setText(QCoreApplication.translate("diary_search_dialog", u"Sort by Date", None))
    # retranslateUi


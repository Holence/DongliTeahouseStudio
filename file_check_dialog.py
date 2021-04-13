# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_check_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_file_check_dialog(object):
    def setupUi(self, file_check_dialog):
        if not file_check_dialog.objectName():
            file_check_dialog.setObjectName(u"file_check_dialog")
        file_check_dialog.resize(949, 685)
        icon = QIcon()
        icon.addFile(u":/icon/holoico_trans.ico", QSize(), QIcon.Normal, QIcon.Off)
        file_check_dialog.setWindowIcon(icon)
        self.horizontalLayout_12 = QHBoxLayout(file_check_dialog)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_quit = QPushButton(file_check_dialog)
        self.pushButton_quit.setObjectName(u"pushButton_quit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_quit.sizePolicy().hasHeightForWidth())
        self.pushButton_quit.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.pushButton_quit)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(file_check_dialog)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setWordWrap(True)

        self.horizontalLayout_8.addWidget(self.label_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_6 = QLabel(file_check_dialog)
        self.label_6.setObjectName(u"label_6")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy2)
        self.label_6.setWordWrap(True)

        self.horizontalLayout_9.addWidget(self.label_6)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)


        self.verticalLayout_3.addLayout(self.verticalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_2 = QLabel(file_check_dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)

        self.verticalLayout_4.addWidget(self.label_2)

        self.splitter = QSplitter(file_check_dialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)
        self.listWidget_missing_file = QListWidget(self.splitter)
        self.listWidget_missing_file.setObjectName(u"listWidget_missing_file")
        self.listWidget_missing_file.setDragEnabled(True)
        self.listWidget_missing_file.setDragDropOverwriteMode(False)
        self.listWidget_missing_file.setDragDropMode(QAbstractItemView.DragOnly)
        self.listWidget_missing_file.setDefaultDropAction(Qt.CopyAction)
        self.listWidget_missing_file.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_missing_file.setSpacing(5)
        self.listWidget_missing_file.setSelectionRectVisible(True)
        self.splitter.addWidget(self.listWidget_missing_file)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_7 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_date = QLineEdit(self.layoutWidget)
        self.lineEdit_date.setObjectName(u"lineEdit_date")
        self.lineEdit_date.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEdit_date.sizePolicy().hasHeightForWidth())
        self.lineEdit_date.setSizePolicy(sizePolicy4)
        self.lineEdit_date.setMinimumSize(QSize(0, 0))
        self.lineEdit_date.setReadOnly(True)

        self.verticalLayout_7.addWidget(self.lineEdit_date)

        self.listWidget_missing_file_related_concept = QListWidget(self.layoutWidget)
        self.listWidget_missing_file_related_concept.setObjectName(u"listWidget_missing_file_related_concept")
        self.listWidget_missing_file_related_concept.setDragEnabled(False)
        self.listWidget_missing_file_related_concept.setDragDropOverwriteMode(False)
        self.listWidget_missing_file_related_concept.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.listWidget_missing_file_related_concept.setDefaultDropAction(Qt.IgnoreAction)
        self.listWidget_missing_file_related_concept.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_missing_file_related_concept.setMovement(QListView.Static)
        self.listWidget_missing_file_related_concept.setFlow(QListView.LeftToRight)
        self.listWidget_missing_file_related_concept.setResizeMode(QListView.Adjust)
        self.listWidget_missing_file_related_concept.setSpacing(5)
        self.listWidget_missing_file_related_concept.setViewMode(QListView.IconMode)
        self.listWidget_missing_file_related_concept.setWordWrap(False)
        self.listWidget_missing_file_related_concept.setSelectionRectVisible(True)

        self.verticalLayout_7.addWidget(self.listWidget_missing_file_related_concept)

        self.splitter.addWidget(self.layoutWidget)

        self.verticalLayout_4.addWidget(self.splitter)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(file_check_dialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.listWidget_redundant_file = QListWidget(file_check_dialog)
        self.listWidget_redundant_file.setObjectName(u"listWidget_redundant_file")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.listWidget_redundant_file.sizePolicy().hasHeightForWidth())
        self.listWidget_redundant_file.setSizePolicy(sizePolicy5)
        self.listWidget_redundant_file.setDragEnabled(True)
        self.listWidget_redundant_file.setDragDropMode(QAbstractItemView.DragOnly)
        self.listWidget_redundant_file.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_redundant_file.setSelectionRectVisible(True)

        self.verticalLayout_2.addWidget(self.listWidget_redundant_file)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(file_check_dialog)
        self.label.setObjectName(u"label")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy6)
        self.label.setTextFormat(Qt.MarkdownText)
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)
        self.label.setMargin(0)

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.label_4 = QLabel(file_check_dialog)
        self.label_4.setObjectName(u"label_4")
        sizePolicy6.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy6)
        self.label_4.setTextFormat(Qt.MarkdownText)
        self.label_4.setWordWrap(True)

        self.horizontalLayout_4.addWidget(self.label_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_erase = QPushButton(file_check_dialog)
        self.pushButton_erase.setObjectName(u"pushButton_erase")
        sizePolicy1.setHeightForWidth(self.pushButton_erase.sizePolicy().hasHeightForWidth())
        self.pushButton_erase.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.pushButton_erase)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_add = QPushButton(file_check_dialog)
        self.pushButton_add.setObjectName(u"pushButton_add")
        sizePolicy1.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy1)
        self.pushButton_add.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout.addWidget(self.pushButton_add)


        self.horizontalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_2 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_4)

        self.label_7 = QLabel(file_check_dialog)
        self.label_7.setObjectName(u"label_7")
        sizePolicy6.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy6)
        self.label_7.setTextFormat(Qt.MarkdownText)
        self.label_7.setScaledContents(True)
        self.label_7.setWordWrap(True)
        self.label_7.setMargin(0)

        self.horizontalLayout_10.addWidget(self.label_7)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget_left = QListWidget(file_check_dialog)
        self.listWidget_left.setObjectName(u"listWidget_left")
        self.listWidget_left.setDragEnabled(True)
        self.listWidget_left.setDragDropMode(QAbstractItemView.DragDrop)
        self.listWidget_left.setDefaultDropAction(Qt.MoveAction)

        self.verticalLayout.addWidget(self.listWidget_left)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_8 = QLabel(file_check_dialog)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_7.addWidget(self.label_8)

        self.pushButton_left_clear = QPushButton(file_check_dialog)
        self.pushButton_left_clear.setObjectName(u"pushButton_left_clear")
        sizePolicy1.setHeightForWidth(self.pushButton_left_clear.sizePolicy().hasHeightForWidth())
        self.pushButton_left_clear.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.pushButton_left_clear)


        self.verticalLayout.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_6.addLayout(self.verticalLayout)

        self.pushButton_replace = QPushButton(file_check_dialog)
        self.pushButton_replace.setObjectName(u"pushButton_replace")

        self.horizontalLayout_6.addWidget(self.pushButton_replace)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.listWidget_right = QListWidget(file_check_dialog)
        self.listWidget_right.setObjectName(u"listWidget_right")
        self.listWidget_right.setDragEnabled(True)
        self.listWidget_right.setDragDropMode(QAbstractItemView.DragDrop)
        self.listWidget_right.setDefaultDropAction(Qt.MoveAction)

        self.verticalLayout_5.addWidget(self.listWidget_right)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = QLabel(file_check_dialog)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_11.addWidget(self.label_9)

        self.pushButton_right_clear = QPushButton(file_check_dialog)
        self.pushButton_right_clear.setObjectName(u"pushButton_right_clear")
        sizePolicy1.setHeightForWidth(self.pushButton_right_clear.sizePolicy().hasHeightForWidth())
        self.pushButton_right_clear.setSizePolicy(sizePolicy1)

        self.horizontalLayout_11.addWidget(self.pushButton_right_clear)


        self.verticalLayout_5.addLayout(self.horizontalLayout_11)


        self.horizontalLayout_6.addLayout(self.verticalLayout_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_12.addLayout(self.verticalLayout_3)

        self.plainTextEdit = QPlainTextEdit(file_check_dialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        sizePolicy5.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy5)
        self.plainTextEdit.setReadOnly(True)

        self.horizontalLayout_12.addWidget(self.plainTextEdit)

        self.horizontalLayout_12.setStretch(0, 4)
        self.horizontalLayout_12.setStretch(1, 1)

        self.retranslateUi(file_check_dialog)

        QMetaObject.connectSlotsByName(file_check_dialog)
    # setupUi

    def retranslateUi(self, file_check_dialog):
        file_check_dialog.setWindowTitle(QCoreApplication.translate("file_check_dialog", u"File Check", None))
        self.pushButton_quit.setText(QCoreApplication.translate("file_check_dialog", u"Quit", None))
        self.label_5.setText(QCoreApplication.translate("file_check_dialog", u"WARNING!!!", None))
        self.label_6.setText(QCoreApplication.translate("file_check_dialog", u"THE OPERATION BELOW IS NOT REVERSIBLE, READ THE DESCRIPTION CAREFULLY AND THINK TWICE BEFORE YOU EXCECUTE! (BACKUP YOU DATA IF NECESSARY)", None))
        self.label_2.setText(QCoreApplication.translate("file_check_dialog", u"Missing Files", None))
        self.label_3.setText(QCoreApplication.translate("file_check_dialog", u"Redundant Files", None))
        self.label.setText(QCoreApplication.translate("file_check_dialog", u"These files are in the file data, but not in the file heap directory.\n"
"\n"
"If you would like to erase all the data (**including file data, concept related file and diary text related file**) related to some of the files you <u>selected</u>, press the button below, and you could add the new file by dragging file into the file manager from somewhere outside the file heap.", None))
        self.label_4.setText(QCoreApplication.translate("file_check_dialog", u"These files are not in the file data, but in the file heap directory.\n"
"\n"
"If you would like to add some of the files you <u>selected</u> into the file data, press the button below, or you should add them properly by dragging file into the file manager from somewhere outside the file heap!", None))
        self.pushButton_erase.setText(QCoreApplication.translate("file_check_dialog", u"ERASE", None))
        self.pushButton_add.setText(QCoreApplication.translate("file_check_dialog", u"ADD", None))
        self.label_7.setText(QCoreApplication.translate("file_check_dialog", u"If you want to replace some of the files in the left list with the ones in the right, then you could drag them to the list below matching each other and execute REPLACE option. All the data linked to the files from the left list (**including file data, concept related file and diary text related file**), will be replaced by the ones in the right list.", None))
        self.label_8.setText(QCoreApplication.translate("file_check_dialog", u"Clear the list if miss placing :(", None))
        self.pushButton_left_clear.setText(QCoreApplication.translate("file_check_dialog", u"Clear", None))
        self.pushButton_replace.setText(QCoreApplication.translate("file_check_dialog", u"REPLACE\n"
"<--", None))
        self.label_9.setText(QCoreApplication.translate("file_check_dialog", u"Clear the list if miss placing :(", None))
        self.pushButton_right_clear.setText(QCoreApplication.translate("file_check_dialog", u"Clear", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("file_check_dialog", u"This is a log.", None))
    # retranslateUi


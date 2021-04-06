# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mytabwidget_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from custom_widget import MyConceptLinkedFileList
from custom_widget import MyTabFileLeafList
from custom_widget import MyPlainTextEdit


class Ui_mytabwidget_form(object):
    def setupUi(self, mytabwidget_form):
        if not mytabwidget_form.objectName():
            mytabwidget_form.setObjectName(u"mytabwidget_form")
        mytabwidget_form.resize(939, 664)
        self.horizontalLayout = QHBoxLayout(mytabwidget_form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter_2 = QSplitter(mytabwidget_form)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.splitter_2.setHandleWidth(10)
        self.treeWidget = QTreeWidget(self.splitter_2)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setTabKeyNavigation(True)
        self.treeWidget.setDragEnabled(False)
        self.treeWidget.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.treeWidget.setAlternatingRowColors(False)
        self.treeWidget.setAutoExpandDelay(50)
        self.treeWidget.setIndentation(20)
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setAnimated(True)
        self.splitter_2.addWidget(self.treeWidget)
        self.treeWidget.header().setVisible(False)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setHandleWidth(10)
        self.splitter_top = QSplitter(self.splitter)
        self.splitter_top.setObjectName(u"splitter_top")
        self.splitter_top.setOrientation(Qt.Horizontal)
        self.splitter_top.setHandleWidth(10)
        self.layoutWidget = QWidget(self.splitter_top)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_id = QLabel(self.layoutWidget)
        self.label_id.setObjectName(u"label_id")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_id)

        self.lineEdit_id = QLineEdit(self.layoutWidget)
        self.lineEdit_id.setObjectName(u"lineEdit_id")
        self.lineEdit_id.setEnabled(True)
        self.lineEdit_id.setMinimumSize(QSize(0, 0))
        self.lineEdit_id.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_id)

        self.label_name = QLabel(self.layoutWidget)
        self.label_name.setObjectName(u"label_name")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_name)

        self.lineEdit_name = QLineEdit(self.layoutWidget)
        self.lineEdit_name.setObjectName(u"lineEdit_name")
        self.lineEdit_name.setMinimumSize(QSize(0, 0))
        self.lineEdit_name.setDragEnabled(False)
        self.lineEdit_name.setReadOnly(False)
        self.lineEdit_name.setClearButtonEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_name)

        self.label_detail = QLabel(self.layoutWidget)
        self.label_detail.setObjectName(u"label_detail")
        sizePolicy.setHeightForWidth(self.label_detail.sizePolicy().hasHeightForWidth())
        self.label_detail.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_detail)

        self.plainTextEdit_detail = MyPlainTextEdit(self.layoutWidget)
        self.plainTextEdit_detail.setObjectName(u"plainTextEdit_detail")
        self.plainTextEdit_detail.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plainTextEdit_detail.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_detail.setSizePolicy(sizePolicy1)
        self.plainTextEdit_detail.setMinimumSize(QSize(0, 0))
        self.plainTextEdit_detail.setMaximumSize(QSize(16777215, 16777215))
        self.plainTextEdit_detail.setReadOnly(False)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.plainTextEdit_detail)

        self.splitter_top.addWidget(self.layoutWidget)
        self.pushButton = QPushButton(self.splitter_top)
        self.pushButton.setObjectName(u"pushButton")
        self.splitter_top.addWidget(self.pushButton)
        self.splitter.addWidget(self.splitter_top)
        self.splitter_bottom = QSplitter(self.splitter)
        self.splitter_bottom.setObjectName(u"splitter_bottom")
        self.splitter_bottom.setOrientation(Qt.Horizontal)
        self.splitter_bottom.setHandleWidth(10)
        self.tabWidget = QTabWidget(self.splitter_bottom)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setLayoutDirection(Qt.LeftToRight)
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget_file_root = MyConceptLinkedFileList(self.tab)
        self.listWidget_file_root.setObjectName(u"listWidget_file_root")
        self.listWidget_file_root.setDragEnabled(True)
        self.listWidget_file_root.setDragDropMode(QAbstractItemView.InternalMove)
        self.listWidget_file_root.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_file_root.setIconSize(QSize(48, 48))
        self.listWidget_file_root.setResizeMode(QListView.Adjust)
        self.listWidget_file_root.setSpacing(16)
        self.listWidget_file_root.setGridSize(QSize(96, 128))
        self.listWidget_file_root.setViewMode(QListView.IconMode)
        self.listWidget_file_root.setWordWrap(True)

        self.verticalLayout.addWidget(self.listWidget_file_root)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget_file_leafs = MyTabFileLeafList(self.tab_2)
        self.listWidget_file_leafs.setObjectName(u"listWidget_file_leafs")
        self.listWidget_file_leafs.setProperty("showDropIndicator", False)
        self.listWidget_file_leafs.setDragDropMode(QAbstractItemView.DragDrop)
        self.listWidget_file_leafs.setDefaultDropAction(Qt.IgnoreAction)
        self.listWidget_file_leafs.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_file_leafs.setIconSize(QSize(48, 48))
        self.listWidget_file_leafs.setMovement(QListView.Free)
        self.listWidget_file_leafs.setResizeMode(QListView.Adjust)
        self.listWidget_file_leafs.setLayoutMode(QListView.Batched)
        self.listWidget_file_leafs.setSpacing(16)
        self.listWidget_file_leafs.setGridSize(QSize(96, 128))
        self.listWidget_file_leafs.setViewMode(QListView.IconMode)
        self.listWidget_file_leafs.setBatchSize(10)
        self.listWidget_file_leafs.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.listWidget_file_leafs)

        self.tabWidget.addTab(self.tab_2, "")
        self.splitter_bottom.addWidget(self.tabWidget)
        self.textEdit_viewer = QTextEdit(self.splitter_bottom)
        self.textEdit_viewer.setObjectName(u"textEdit_viewer")
        self.textEdit_viewer.setReadOnly(True)
        self.splitter_bottom.addWidget(self.textEdit_viewer)
        self.splitter.addWidget(self.splitter_bottom)
        self.splitter_2.addWidget(self.splitter)

        self.horizontalLayout.addWidget(self.splitter_2)


        self.retranslateUi(mytabwidget_form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(mytabwidget_form)
    # setupUi

    def retranslateUi(self, mytabwidget_form):
        mytabwidget_form.setWindowTitle(QCoreApplication.translate("mytabwidget_form", u"Form", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("mytabwidget_form", u"New Column", None));
        self.label_id.setText(QCoreApplication.translate("mytabwidget_form", u"ID", None))
        self.label_name.setText(QCoreApplication.translate("mytabwidget_form", u"Name", None))
        self.label_detail.setText(QCoreApplication.translate("mytabwidget_form", u"Detail", None))
        self.plainTextEdit_detail.setPlainText("")
        self.pushButton.setText(QCoreApplication.translate("mytabwidget_form", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("mytabwidget_form", u"Root", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("mytabwidget_form", u"Leaf", None))
        self.textEdit_viewer.setHtml(QCoreApplication.translate("mytabwidget_form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt;\"><br /></p></body></html>", None))
    # retranslateUi


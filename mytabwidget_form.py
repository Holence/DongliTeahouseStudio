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


class Ui_mytabwidget_form(object):
    def setupUi(self, mytabwidget_form):
        if not mytabwidget_form.objectName():
            mytabwidget_form.setObjectName(u"mytabwidget_form")
        mytabwidget_form.resize(705, 627)
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
        self.listWidget_file_root = MyConceptLinkedFileList(self.splitter)
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
        self.splitter.addWidget(self.listWidget_file_root)
        self.listWidget_file_leafs = MyTabFileLeafList(self.splitter)
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
        self.splitter.addWidget(self.listWidget_file_leafs)
        self.splitter_2.addWidget(self.splitter)

        self.horizontalLayout.addWidget(self.splitter_2)


        self.retranslateUi(mytabwidget_form)

        QMetaObject.connectSlotsByName(mytabwidget_form)
    # setupUi

    def retranslateUi(self, mytabwidget_form):
        mytabwidget_form.setWindowTitle(QCoreApplication.translate("mytabwidget_form", u"Form", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("mytabwidget_form", u"New Column", None));
    # retranslateUi


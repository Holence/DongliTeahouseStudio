# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'diary_analyze_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_diary_analyze_dialog(object):
    def setupUi(self, diary_analyze_dialog):
        if not diary_analyze_dialog.objectName():
            diary_analyze_dialog.setObjectName(u"diary_analyze_dialog")
        diary_analyze_dialog.resize(541, 506)
        self.verticalLayout = QVBoxLayout(diary_analyze_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter_2 = QSplitter(diary_analyze_dialog)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter_2.setHandleWidth(10)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.dateEdit_end = QDateEdit(self.layoutWidget)
        self.dateEdit_end.setObjectName(u"dateEdit_end")
        self.dateEdit_end.setMaximumDate(QDate(2169, 12, 31))
        self.dateEdit_end.setMinimumDate(QDate(1970, 1, 1))

        self.gridLayout.addWidget(self.dateEdit_end, 1, 2, 1, 1)

        self.dateEdit_begin = QDateEdit(self.layoutWidget)
        self.dateEdit_begin.setObjectName(u"dateEdit_begin")
        self.dateEdit_begin.setMaximumDateTime(QDateTime(QDate(2169, 12, 31), QTime(23, 59, 59)))
        self.dateEdit_begin.setMinimumDateTime(QDateTime(QDate(1970, 1, 1), QTime(0, 0, 0)))

        self.gridLayout.addWidget(self.dateEdit_begin, 1, 1, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)

        self.comboBox = QComboBox(self.layoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)

        self.pushButton_analyze = QPushButton(self.layoutWidget)
        self.pushButton_analyze.setObjectName(u"pushButton_analyze")

        self.gridLayout.addWidget(self.pushButton_analyze, 1, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 2)
        self.splitter_2.addWidget(self.layoutWidget)
        self.horizontalLayoutWidget = QWidget(self.splitter_2)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayout_chart = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_chart.setObjectName(u"horizontalLayout_chart")
        self.horizontalLayout_chart.setContentsMargins(0, 0, 0, 0)
        self.splitter_2.addWidget(self.horizontalLayoutWidget)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.listWidget_all_concept = QListWidget(self.splitter)
        self.listWidget_all_concept.setObjectName(u"listWidget_all_concept")
        self.splitter.addWidget(self.listWidget_all_concept)
        self.textEdit_viewer = QTextEdit(self.splitter)
        self.textEdit_viewer.setObjectName(u"textEdit_viewer")
        self.textEdit_viewer.setReadOnly(True)
        self.splitter.addWidget(self.textEdit_viewer)
        self.splitter_2.addWidget(self.splitter)

        self.verticalLayout.addWidget(self.splitter_2)


        self.retranslateUi(diary_analyze_dialog)

        QMetaObject.connectSlotsByName(diary_analyze_dialog)
    # setupUi

    def retranslateUi(self, diary_analyze_dialog):
        diary_analyze_dialog.setWindowTitle(QCoreApplication.translate("diary_analyze_dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("diary_analyze_dialog", u"From", None))
        self.label_2.setText(QCoreApplication.translate("diary_analyze_dialog", u"To", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("diary_analyze_dialog", u"Custome", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("diary_analyze_dialog", u"Week", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("diary_analyze_dialog", u"Month", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("diary_analyze_dialog", u"Year", None))

        self.pushButton_analyze.setText(QCoreApplication.translate("diary_analyze_dialog", u"Analyze", None))
        self.textEdit_viewer.setHtml(QCoreApplication.translate("diary_analyze_dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:18pt;\"><br /></p></body></html>", None))
    # retranslateUi


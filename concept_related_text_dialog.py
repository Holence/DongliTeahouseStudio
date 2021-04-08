# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'concept_related_text_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc

class Ui_concept_related_text_dialog(object):
    def setupUi(self, concept_related_text_dialog):
        if not concept_related_text_dialog.objectName():
            concept_related_text_dialog.setObjectName(u"concept_related_text_dialog")
        concept_related_text_dialog.resize(678, 515)
        icon = QIcon()
        icon.addFile(u":/icon/holoico.ico", QSize(), QIcon.Normal, QIcon.Off)
        concept_related_text_dialog.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(concept_related_text_dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_5 = QLabel(concept_related_text_dialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_6 = QLabel(concept_related_text_dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.lineEdit_source_id = QLineEdit(concept_related_text_dialog)
        self.lineEdit_source_id.setObjectName(u"lineEdit_source_id")
        self.lineEdit_source_id.setReadOnly(True)

        self.gridLayout_3.addWidget(self.lineEdit_source_id, 1, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(concept_related_text_dialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEdit_target_id = QLineEdit(concept_related_text_dialog)
        self.lineEdit_target_id.setObjectName(u"lineEdit_target_id")

        self.gridLayout_2.addWidget(self.lineEdit_target_id, 1, 1, 1, 1)

        self.label_3 = QLabel(concept_related_text_dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 2, 1, 1)

        self.listWidget_source = QListWidget(concept_related_text_dialog)
        self.listWidget_source.setObjectName(u"listWidget_source")
        self.listWidget_source.setDragDropMode(QAbstractItemView.DragOnly)
        self.listWidget_source.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_source.setSpacing(10)

        self.gridLayout_4.addWidget(self.listWidget_source, 1, 0, 1, 1)

        self.label_4 = QLabel(concept_related_text_dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(146, 16777215))
        self.label_4.setTextFormat(Qt.AutoText)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)

        self.gridLayout_4.addWidget(self.label_4, 1, 1, 1, 1)

        self.listWidget_target = QListWidget(concept_related_text_dialog)
        self.listWidget_target.setObjectName(u"listWidget_target")
        self.listWidget_target.setDragDropMode(QAbstractItemView.DropOnly)
        self.listWidget_target.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listWidget_target.setSpacing(10)

        self.gridLayout_4.addWidget(self.listWidget_target, 1, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(concept_related_text_dialog)
        self.label.setObjectName(u"label")
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_delete = QPushButton(concept_related_text_dialog)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_delete.sizePolicy().hasHeightForWidth())
        self.pushButton_delete.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.pushButton_delete)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.gridLayout_4.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(concept_related_text_dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setWordWrap(True)

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_8 = QLabel(concept_related_text_dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)
        self.label_8.setWordWrap(True)

        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_remove = QPushButton(concept_related_text_dialog)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        sizePolicy.setHeightForWidth(self.pushButton_remove.sizePolicy().hasHeightForWidth())
        self.pushButton_remove.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton_remove)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_copy = QPushButton(concept_related_text_dialog)
        self.pushButton_copy.setObjectName(u"pushButton_copy")
        sizePolicy.setHeightForWidth(self.pushButton_copy.sizePolicy().hasHeightForWidth())
        self.pushButton_copy.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.pushButton_copy)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 2, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_4)


        self.retranslateUi(concept_related_text_dialog)

        QMetaObject.connectSlotsByName(concept_related_text_dialog)
    # setupUi

    def retranslateUi(self, concept_related_text_dialog):
        concept_related_text_dialog.setWindowTitle(QCoreApplication.translate("concept_related_text_dialog", u"Edit Concept Related Text", None))
        self.label_5.setText(QCoreApplication.translate("concept_related_text_dialog", u"Source Concept", None))
        self.label_6.setText(QCoreApplication.translate("concept_related_text_dialog", u"Concept ID:", None))
        self.label_2.setText(QCoreApplication.translate("concept_related_text_dialog", u"Target Concept", None))
        self.label_3.setText(QCoreApplication.translate("concept_related_text_dialog", u"Concept ID:", None))
        self.label_4.setText(QCoreApplication.translate("concept_related_text_dialog", u"THE OPERATION BELOW IS NOT REVERSIBLE, READ THE DESCRIPTION CAREFULLY AND THINK TWICE BEFORE YOU EXCECUTE! (BACKUP YOU DATA IF NECESSARY)\n"
"\n"
"\n"
"---------------->\n"
"\n"
"\n"
"Drag text to right to perform Copy.", None))
        self.label.setText(QCoreApplication.translate("concept_related_text_dialog", u"Delete texts linked to Souce Concept in bulk.", None))
        self.pushButton_delete.setText(QCoreApplication.translate("concept_related_text_dialog", u"Delete", None))
        self.label_7.setText(QCoreApplication.translate("concept_related_text_dialog", u"If you have missed placing the some of the text, select them and press Remove.", None))
        self.label_8.setText(QCoreApplication.translate("concept_related_text_dialog", u"If you want to add these text linked to Target Concept, press Copy Confirm.", None))
        self.pushButton_remove.setText(QCoreApplication.translate("concept_related_text_dialog", u"Remove", None))
        self.pushButton_copy.setText(QCoreApplication.translate("concept_related_text_dialog", u"Copy Confirm", None))
    # retranslateUi


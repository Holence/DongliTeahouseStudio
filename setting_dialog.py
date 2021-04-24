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
        setting_dialog.resize(722, 583)
        icon = QIcon()
        icon.addFile(u":/icon/holoico_trans.ico", QSize(), QIcon.Normal, QIcon.Off)
        setting_dialog.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(setting_dialog)
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

        self.pushButton_home = QPushButton(setting_dialog)
        self.pushButton_home.setObjectName(u"pushButton_home")
        icon2 = QIcon()
        icon2.addFile(u":/icon/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_home.setIcon(icon2)
        self.pushButton_home.setIconSize(QSize(32, 32))
        self.pushButton_home.setFlat(True)

        self.verticalLayout_4.addWidget(self.pushButton_home)

        self.pushButton_rss = QPushButton(setting_dialog)
        self.pushButton_rss.setObjectName(u"pushButton_rss")
        icon3 = QIcon()
        icon3.addFile(u":/icon/rss.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_rss.setIcon(icon3)
        self.pushButton_rss.setIconSize(QSize(32, 32))
        self.pushButton_rss.setFlat(True)

        self.verticalLayout_4.addWidget(self.pushButton_rss)

        self.pushButton_zen = QPushButton(setting_dialog)
        self.pushButton_zen.setObjectName(u"pushButton_zen")
        icon4 = QIcon()
        icon4.addFile(u":/icon/moon.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_zen.setIcon(icon4)
        self.pushButton_zen.setIconSize(QSize(32, 32))
        self.pushButton_zen.setFlat(True)

        self.verticalLayout_4.addWidget(self.pushButton_zen)

        self.pushButton_library = QPushButton(setting_dialog)
        self.pushButton_library.setObjectName(u"pushButton_library")
        icon5 = QIcon()
        icon5.addFile(u":/icon/hard-drive.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_library.setIcon(icon5)
        self.pushButton_library.setIconSize(QSize(32, 32))
        self.pushButton_library.setFlat(True)

        self.verticalLayout_4.addWidget(self.pushButton_library)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget = QStackedWidget(setting_dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"")
        self.page_general = QWidget()
        self.page_general.setObjectName(u"page_general")
        self.page_general.setMaximumSize(QSize(16777215, 240))
        self.gridLayout = QGridLayout(self.page_general)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.page_general)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_9 = QLabel(self.page_general)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)

        self.lineEdit_backup_directory = QLineEdit(self.page_general)
        self.lineEdit_backup_directory.setObjectName(u"lineEdit_backup_directory")
        self.lineEdit_backup_directory.setEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_backup_directory, 5, 0, 1, 1)

        self.lineEdit_password = QLineEdit(self.page_general)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setEnabled(True)

        self.gridLayout.addWidget(self.lineEdit_password, 7, 0, 1, 1)

        self.pushButton_change_password = QPushButton(self.page_general)
        self.pushButton_change_password.setObjectName(u"pushButton_change_password")

        self.gridLayout.addWidget(self.pushButton_change_password, 7, 1, 1, 1)

        self.lineEdit_font = QLineEdit(self.page_general)
        self.lineEdit_font.setObjectName(u"lineEdit_font")
        self.lineEdit_font.setEnabled(False)
        self.lineEdit_font.setReadOnly(False)

        self.gridLayout.addWidget(self.lineEdit_font, 1, 0, 1, 1)

        self.pushButton_font = QPushButton(self.page_general)
        self.pushButton_font.setObjectName(u"pushButton_font")

        self.gridLayout.addWidget(self.pushButton_font, 1, 1, 1, 1)

        self.label_10 = QLabel(self.page_general)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 1)

        self.checkBox_auto_backup = QCheckBox(self.page_general)
        self.checkBox_auto_backup.setObjectName(u"checkBox_auto_backup")
        self.checkBox_auto_backup.setLayoutDirection(Qt.RightToLeft)

        self.gridLayout.addWidget(self.checkBox_auto_backup, 5, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_general)
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_3 = QGridLayout(self.page_home)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_8 = QLabel(self.page_home)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)

        self.lineEdit_random_text = QLineEdit(self.page_home)
        self.lineEdit_random_text.setObjectName(u"lineEdit_random_text")
        self.lineEdit_random_text.setEnabled(False)

        self.gridLayout_3.addWidget(self.lineEdit_random_text, 1, 0, 1, 1)

        self.pushButton_random_text = QPushButton(self.page_home)
        self.pushButton_random_text.setObjectName(u"pushButton_random_text")

        self.gridLayout_3.addWidget(self.pushButton_random_text, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_home)
        self.page_rss = QWidget()
        self.page_rss.setObjectName(u"page_rss")
        self.page_rss.setMaximumSize(QSize(16777215, 120))
        self.gridLayout_2 = QGridLayout(self.page_rss)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineEdit_instagram_cookie = QLineEdit(self.page_rss)
        self.lineEdit_instagram_cookie.setObjectName(u"lineEdit_instagram_cookie")

        self.gridLayout_2.addWidget(self.lineEdit_instagram_cookie, 1, 1, 1, 1)

        self.label_4 = QLabel(self.page_rss)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_3 = QLabel(self.page_rss)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEdit_pixiv_cookie = QLineEdit(self.page_rss)
        self.lineEdit_pixiv_cookie.setObjectName(u"lineEdit_pixiv_cookie")

        self.gridLayout_2.addWidget(self.lineEdit_pixiv_cookie, 0, 1, 1, 1)

        self.checkBox_rss_auto_update = QCheckBox(self.page_rss)
        self.checkBox_rss_auto_update.setObjectName(u"checkBox_rss_auto_update")
        self.checkBox_rss_auto_update.setLayoutDirection(Qt.RightToLeft)

        self.gridLayout_2.addWidget(self.checkBox_rss_auto_update, 2, 1, 1, 1)

        self.label_5 = QLabel(self.page_rss)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_rss)
        self.page_zen = QWidget()
        self.page_zen.setObjectName(u"page_zen")
        self.page_zen.setMaximumSize(QSize(16777215, 160))
        self.gridLayout_4 = QGridLayout(self.page_zen)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_7 = QLabel(self.page_zen)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)

        self.lineEdit_sublime = QLineEdit(self.page_zen)
        self.lineEdit_sublime.setObjectName(u"lineEdit_sublime")
        self.lineEdit_sublime.setEnabled(False)

        self.gridLayout_4.addWidget(self.lineEdit_sublime, 1, 0, 1, 1)

        self.pushButton_sublime = QPushButton(self.page_zen)
        self.pushButton_sublime.setObjectName(u"pushButton_sublime")

        self.gridLayout_4.addWidget(self.pushButton_sublime, 1, 1, 1, 1)

        self.label_6 = QLabel(self.page_zen)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 2)

        self.lineEdit_typora = QLineEdit(self.page_zen)
        self.lineEdit_typora.setObjectName(u"lineEdit_typora")
        self.lineEdit_typora.setEnabled(False)

        self.gridLayout_4.addWidget(self.lineEdit_typora, 3, 0, 1, 1)

        self.pushButton_typora = QPushButton(self.page_zen)
        self.pushButton_typora.setObjectName(u"pushButton_typora")

        self.gridLayout_4.addWidget(self.pushButton_typora, 3, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_zen)
        self.page_library = QWidget()
        self.page_library.setObjectName(u"page_library")
        self.page_library.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_5 = QGridLayout(self.page_library)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label = QLabel(self.page_library)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_file_saving_base = QLineEdit(self.page_library)
        self.lineEdit_file_saving_base.setObjectName(u"lineEdit_file_saving_base")
        self.lineEdit_file_saving_base.setEnabled(False)

        self.gridLayout_5.addWidget(self.lineEdit_file_saving_base, 1, 0, 1, 1)

        self.pushButtonfile_saving_base = QPushButton(self.page_library)
        self.pushButtonfile_saving_base.setObjectName(u"pushButtonfile_saving_base")

        self.gridLayout_5.addWidget(self.pushButtonfile_saving_base, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_library)

        self.verticalLayout_3.addWidget(self.stackedWidget)

        self.buttonBox = QDialogButtonBox(setting_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.retranslateUi(setting_dialog)
        self.buttonBox.accepted.connect(setting_dialog.accept)
        self.buttonBox.rejected.connect(setting_dialog.reject)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(setting_dialog)
    # setupUi

    def retranslateUi(self, setting_dialog):
        setting_dialog.setWindowTitle(QCoreApplication.translate("setting_dialog", u"Setting", None))
        self.pushButton_general.setText("")
        self.pushButton_home.setText("")
        self.pushButton_rss.setText("")
        self.pushButton_zen.setText("")
        self.pushButton_library.setText("")
        self.label_2.setText(QCoreApplication.translate("setting_dialog", u"Font", None))
        self.label_9.setText(QCoreApplication.translate("setting_dialog", u"Password", None))
        self.lineEdit_backup_directory.setPlaceholderText(QCoreApplication.translate("setting_dialog", u"C:\\Users\\Holence\\OneDrive\\DataBackup;", None))
        self.pushButton_change_password.setText(QCoreApplication.translate("setting_dialog", u"Change", None))
        self.pushButton_font.setText(QCoreApplication.translate("setting_dialog", u"Font...", None))
        self.label_10.setText(QCoreApplication.translate("setting_dialog", u"Backup Directory\uff08\u7528\u82f1\u6587\u5206\u53f7\u9694\u5f00\uff09", None))
        self.checkBox_auto_backup.setText(QCoreApplication.translate("setting_dialog", u"\u542f\u52a8\u65f6\u81ea\u52a8\u5907\u4efd", None))
        self.label_8.setText(QCoreApplication.translate("setting_dialog", u"Random Text Directory", None))
        self.pushButton_random_text.setText(QCoreApplication.translate("setting_dialog", u"Open...", None))
        self.label_4.setText(QCoreApplication.translate("setting_dialog", u"Instagram Cookie\uff08Instagram\u662f\u4e0d\u5bf9\u5916\u5f00\u653e\u7684\uff09", None))
        self.label_3.setText(QCoreApplication.translate("setting_dialog", u"Pixiv Cookie\uff08\u4e00\u4e9b\u753b\u5e08\u7684\u9650\u5236\u6bd4\u8f83\u4e25\u683c\uff0c\u9700\u8981cookie\u624d\u80fd\u8bbf\u95ee\u5230\uff09", None))
        self.checkBox_rss_auto_update.setText("")
        self.label_5.setText(QCoreApplication.translate("setting_dialog", u"\u6bcf\u65e5\u81ea\u52a8\u66f4\u65b0", None))
        self.label_7.setText(QCoreApplication.translate("setting_dialog", u"Sublime Directory", None))
        self.pushButton_sublime.setText(QCoreApplication.translate("setting_dialog", u"Open...", None))
        self.label_6.setText(QCoreApplication.translate("setting_dialog", u"Typora Directory", None))
        self.pushButton_typora.setText(QCoreApplication.translate("setting_dialog", u"Open...", None))
        self.label.setText(QCoreApplication.translate("setting_dialog", u"File Saving Directory", None))
        self.pushButtonfile_saving_base.setText(QCoreApplication.translate("setting_dialog", u"Open...", None))
    # retranslateUi


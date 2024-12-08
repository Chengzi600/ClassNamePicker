# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pyqt5ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(700, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"QCheckBox\n"
"{\n"
"	border-radius:9px;\n"
"	border:1px solid blue;\n"
"}\n"
"QCheckBox::hover::unchecked\n"
"{\n"
"	border-radius:9px;\n"
"	border:1px solid black;\n"
"	background:red;\n"
"	color:white;\n"
"}\n"
"QCheckBox::checked\n"
"{\n"
"	border-radius:9px;\n"
"	border:1px solid black;\n"
"	background:rgb(0, 255, 0);\n"
"	color:white;\n"
"}\n"
"QCheckBox::disabled\n"
"{\n"
"	color:rgba(180, 180, 180, 220);\n"
"	background:rgba(110, 110, 110, 150);\n"
"}\n"
"QPushButton::disabled\n"
"{\n"
"	color:rgba(180, 180, 180, 220);\n"
"	background:rgba(110, 110, 110, 150);\n"
"}\n"
"QPushButton[text=\"重置名单\"],QPushButton[text=\">>> 抽取 <<<\"]\n"
"{\n"
"	border-radius:9px;\n"
"	border:1px solid blue;\n"
"}\n"
"QPushButton::hover[text=\"重置名单\"],QPushButton::hover[text=\">>> 抽取 <<<\"]\n"
"{\n"
"	border-radius:9px;\n"
"	border:1px solid black;\n"
"	background:red;\n"
"	color:white;\n"
"}")
        self.update_action = QAction(MainWindow)
        self.update_action.setObjectName(u"update_action")
        self.about_action = QAction(MainWindow)
        self.about_action.setObjectName(u"about_action")
        self.github_action = QAction(MainWindow)
        self.github_action.setObjectName(u"github_action")
        self.exit_action = QAction(MainWindow)
        self.exit_action.setObjectName(u"exit_action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Main_ui = QVBoxLayout()
        self.Main_ui.setObjectName(u"Main_ui")
        self.main_ui = QVBoxLayout()
        self.main_ui.setSpacing(10)
        self.main_ui.setObjectName(u"main_ui")
        self.main_ui.setContentsMargins(0, 0, -1, -1)
        self.name_label = QLabel(self.centralwidget)
        self.name_label.setObjectName(u"name_label")
        sizePolicy.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setPointSize(88)
        self.name_label.setFont(font)
        self.name_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.name_label.setStyleSheet(u"border-radius:9px;\n"
"border:1px solid white;\n"
"color:qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));background-color:rgba(245,245,245,225);")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_ui.addWidget(self.name_label)

        self.pick_name_button = QPushButton(self.centralwidget)
        self.pick_name_button.setObjectName(u"pick_name_button")
        font1 = QFont()
        font1.setFamily(u"\u9ed1\u4f53")
        font1.setPointSize(22)
        self.pick_name_button.setFont(font1)
        self.pick_name_button.setStyleSheet(u"QPushButton {\n"
"    padding: 20px;\n"
"}\n"
"")

        self.main_ui.addWidget(self.pick_name_button)

        self.reset_button = QPushButton(self.centralwidget)
        self.reset_button.setObjectName(u"reset_button")
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        brush2 = QBrush(QColor(127, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        brush3 = QBrush(QColor(170, 170, 170, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        brush4 = QBrush(QColor(255, 0, 0, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        brush5 = QBrush(QColor(255, 255, 220, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush5)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush6 = QBrush(QColor(255, 0, 0, 128))
        brush6.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush6)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush6)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        brush7 = QBrush(QColor(0, 0, 0, 128))
        brush7.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush7)
#endif
        self.reset_button.setPalette(palette)
        font2 = QFont()
        font2.setFamily(u"\u9ed1\u4f53")
        font2.setPointSize(18)
        self.reset_button.setFont(font2)
        self.reset_button.setStyleSheet(u"QPushButton {\n"
"    padding: 10px;\n"
"}\n"
"")

        self.main_ui.addWidget(self.reset_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.main_ui.addItem(self.verticalSpacer)

        self.main_ui.setStretch(0, 50)

        self.Main_ui.addLayout(self.main_ui)

        self.config_ui = QVBoxLayout()
        self.config_ui.setObjectName(u"config_ui")
        self.config_ui_1 = QHBoxLayout()
        self.config_ui_1.setSpacing(7)
        self.config_ui_1.setObjectName(u"config_ui_1")
        self.config_ui_1.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.config_ui_1.setContentsMargins(30, -1, -1, -1)
        self.n_pick_checkbox = QCheckBox(self.centralwidget)
        self.n_pick_checkbox.setObjectName(u"n_pick_checkbox")
        self.n_pick_checkbox.setEnabled(False)
        self.n_pick_checkbox.setMinimumSize(QSize(117, 18))
        font3 = QFont()
        font3.setFamily(u"\u5b8b\u4f53")
        font3.setPointSize(12)
        self.n_pick_checkbox.setFont(font3)
        self.n_pick_checkbox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.n_pick_checkbox.setCheckable(True)

        self.config_ui_1.addWidget(self.n_pick_checkbox)

        self.g_names_pick_checkbox = QCheckBox(self.centralwidget)
        self.g_names_pick_checkbox.setObjectName(u"g_names_pick_checkbox")
        self.g_names_pick_checkbox.setMinimumSize(QSize(117, 18))
        self.g_names_pick_checkbox.setFont(font3)
        self.g_names_pick_checkbox.setChecked(False)

        self.config_ui_1.addWidget(self.g_names_pick_checkbox)

        self.b_names_pick_checkbox = QCheckBox(self.centralwidget)
        self.b_names_pick_checkbox.setObjectName(u"b_names_pick_checkbox")
        self.b_names_pick_checkbox.setMinimumSize(QSize(117, 18))
        self.b_names_pick_checkbox.setFont(font3)
        self.b_names_pick_checkbox.setChecked(False)
        self.b_names_pick_checkbox.setTristate(False)

        self.config_ui_1.addWidget(self.b_names_pick_checkbox)


        self.config_ui.addLayout(self.config_ui_1)

        self.config_ui_2 = QHBoxLayout()
        self.config_ui_2.setSpacing(7)
        self.config_ui_2.setObjectName(u"config_ui_2")
        self.config_ui_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.config_ui_2.setContentsMargins(30, -1, -1, -1)
        self.pick_again_checkbox = QCheckBox(self.centralwidget)
        self.pick_again_checkbox.setObjectName(u"pick_again_checkbox")
        self.pick_again_checkbox.setMinimumSize(QSize(117, 18))
        self.pick_again_checkbox.setFont(font3)
        self.pick_again_checkbox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.config_ui_2.addWidget(self.pick_again_checkbox)

        self.pick_time_checkbox = QCheckBox(self.centralwidget)
        self.pick_time_checkbox.setObjectName(u"pick_time_checkbox")
        self.pick_time_checkbox.setMinimumSize(QSize(117, 18))
        self.pick_time_checkbox.setFont(font3)

        self.config_ui_2.addWidget(self.pick_time_checkbox)

        self.pick_read_checkbox = QCheckBox(self.centralwidget)
        self.pick_read_checkbox.setObjectName(u"pick_read_checkbox")
        self.pick_read_checkbox.setMinimumSize(QSize(117, 18))
        self.pick_read_checkbox.setFont(font3)

        self.config_ui_2.addWidget(self.pick_read_checkbox)


        self.config_ui.addLayout(self.config_ui_2)

        self.config_ui_3 = QHBoxLayout()
        self.config_ui_3.setSpacing(7)
        self.config_ui_3.setObjectName(u"config_ui_3")
        self.config_ui_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.config_ui_3.setContentsMargins(30, -1, -1, -1)
        self.pick_animation_checkbox = QCheckBox(self.centralwidget)
        self.pick_animation_checkbox.setObjectName(u"pick_animation_checkbox")
        self.pick_animation_checkbox.setMinimumSize(QSize(117, 18))
        self.pick_animation_checkbox.setFont(font3)
        self.pick_animation_checkbox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.config_ui_3.addWidget(self.pick_animation_checkbox)

        self.is_save_checkbox = QCheckBox(self.centralwidget)
        self.is_save_checkbox.setObjectName(u"is_save_checkbox")
        self.is_save_checkbox.setMinimumSize(QSize(117, 18))
        self.is_save_checkbox.setFont(font3)

        self.config_ui_3.addWidget(self.is_save_checkbox)

        self.checkBox_12 = QCheckBox(self.centralwidget)
        self.checkBox_12.setObjectName(u"checkBox_12")
        self.checkBox_12.setEnabled(False)
        self.checkBox_12.setMinimumSize(QSize(117, 18))
        self.checkBox_12.setFont(font3)
        self.checkBox_12.setChecked(False)

        self.config_ui_3.addWidget(self.checkBox_12)


        self.config_ui.addLayout(self.config_ui_3)


        self.Main_ui.addLayout(self.config_ui)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.timer_label = QLabel(self.centralwidget)
        self.timer_label.setObjectName(u"timer_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.timer_label.sizePolicy().hasHeightForWidth())
        self.timer_label.setSizePolicy(sizePolicy1)
        self.timer_label.setMinimumSize(QSize(61, 81))
        self.timer_label.setStyleSheet(u"border-radius:9px;\n"
"border:1px solid white;\n"
"color:qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));background:rgba(245,245,245,225);")
        font4 = QFont()
        font4.setFamily(u"Times New Roman")
        font4.setPointSize(68)
        self.timer_label.setFont(font4)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.timer_label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.Main_ui.addLayout(self.verticalLayout)

        self.Main_ui.setStretch(0, 12)
        self.Main_ui.setStretch(1, 12)
        self.Main_ui.setStretch(2, 12)

        self.verticalLayout_2.addLayout(self.Main_ui)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 552, 21))
        self.menu_about = QMenu(self.menubar)
        self.menu_about.setObjectName(u"menu_about")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_about.menuAction())
        self.menu_about.addAction(self.about_action)
        self.menu_about.addAction(self.exit_action)
        self.menu_about.addSeparator()
        self.menu_about.addAction(self.update_action)
        self.menu_about.addAction(self.github_action)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.update_action.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u67e5\u66f4\u65b0", None))
        self.about_action.setText(QCoreApplication.translate("MainWindow", u"\u7a0b\u5e8f\u7b80\u4ecb", None))
        self.github_action.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00 Github \u4ed3\u5e93", None))
        self.exit_action.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa\u7a0b\u5e8f", None))
        self.name_label.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u62bd\u53d6", None))
        self.pick_name_button.setText(QCoreApplication.translate("MainWindow", u">>> \u62bd\u53d6 <<<", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u540d\u5355", None))
        self.n_pick_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u5747\u8861\u6a21\u5f0f", None))
        self.g_names_pick_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u53ea\u62bd\u5973\u751f", None))
        self.b_names_pick_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u53ea\u62bd\u7537\u751f", None))
        self.pick_again_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u5141\u8bb8\u91cd\u590d\u62bd\u53d6", None))
        self.pick_time_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u8ba1\u65f6\u5668", None))
        self.pick_read_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f\u64ad\u62a5(\u6d4b\u8bd5)", None))
        self.pick_animation_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u542f\u52a8\u753b", None))
        self.is_save_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa\u4fdd\u5b58", None))
        self.checkBox_12.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u53d1\u4e2d...", None))
        self.timer_label.setText(QCoreApplication.translate("MainWindow", u"0.0s", None))
        self.menu_about.setTitle(QCoreApplication.translate("MainWindow", u"\u7a0b\u5e8f", None))
    # retranslateUi


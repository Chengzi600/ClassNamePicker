# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/config.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfigMainWindow(object):
    def setupUi(self, ConfigMainWindow):
        ConfigMainWindow.setObjectName("ConfigMainWindow")
        ConfigMainWindow.resize(679, 486)
        self.centralwidget = QtWidgets.QWidget(ConfigMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.float_chackbox = QtWidgets.QCheckBox(self.groupBox)
        self.float_chackbox.setObjectName("float_chackbox")
        self.gridLayout.addWidget(self.float_chackbox, 1, 2, 1, 1)
        self.save_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.save_checkbox.setObjectName("save_checkbox")
        self.gridLayout.addWidget(self.save_checkbox, 1, 1, 1, 1)
        self.gname_button = QtWidgets.QPushButton(self.groupBox)
        self.gname_button.setObjectName("gname_button")
        self.gridLayout.addWidget(self.gname_button, 0, 2, 1, 1)
        self.speak_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.speak_checkbox.setObjectName("speak_checkbox")
        self.gridLayout.addWidget(self.speak_checkbox, 1, 0, 1, 1)
        self.name_button = QtWidgets.QPushButton(self.groupBox)
        self.name_button.setObjectName("name_button")
        self.gridLayout.addWidget(self.name_button, 0, 1, 1, 1)
        self.update_button = QtWidgets.QPushButton(self.groupBox)
        self.update_button.setObjectName("update_button")
        self.gridLayout.addWidget(self.update_button, 0, 0, 1, 1)
        self.animation_checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.animation_checkBox.setObjectName("animation_checkBox")
        self.gridLayout.addWidget(self.animation_checkBox, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.ani_time_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.ani_time_edit.setInputMask("")
        self.ani_time_edit.setObjectName("ani_time_edit")
        self.gridLayout_2.addWidget(self.ani_time_edit, 0, 3, 1, 1)
        self.a1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.a1.setObjectName("a1")
        self.gridLayout_2.addWidget(self.a1, 5, 1, 1, 1)
        self.b1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.b1.setObjectName("b1")
        self.gridLayout_2.addWidget(self.b1, 6, 1, 1, 1)
        self.b2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.b2.setObjectName("b2")
        self.gridLayout_2.addWidget(self.b2, 6, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 5, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 7, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 4, 1, 1)
        self.c2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.c2.setObjectName("c2")
        self.gridLayout_2.addWidget(self.c2, 7, 3, 1, 1)
        self.c1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.c1.setObjectName("c1")
        self.gridLayout_2.addWidget(self.c1, 7, 1, 1, 1)
        self.a2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.a2.setObjectName("a2")
        self.gridLayout_2.addWidget(self.a2, 5, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 1, 1, 1)
        self.floatsize_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.floatsize_edit.setInputMask("")
        self.floatsize_edit.setObjectName("floatsize_edit")
        self.gridLayout_2.addWidget(self.floatsize_edit, 1, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 2, 1, 1, 1)
        self.speed_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.speed_edit.setObjectName("speed_edit")
        self.gridLayout_2.addWidget(self.speed_edit, 2, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        ConfigMainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ConfigMainWindow)
        QtCore.QMetaObject.connectSlotsByName(ConfigMainWindow)

    def retranslateUi(self, ConfigMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ConfigMainWindow.setWindowTitle(_translate("ConfigMainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("ConfigMainWindow", "基本"))
        self.float_chackbox.setText(_translate("ConfigMainWindow", "显示悬浮窗"))
        self.save_checkbox.setText(_translate("ConfigMainWindow", "自动保存进度"))
        self.gname_button.setText(_translate("ConfigMainWindow", "配置女生名单"))
        self.speak_checkbox.setText(_translate("ConfigMainWindow", "语音播报"))
        self.name_button.setText(_translate("ConfigMainWindow", "配置总名单"))
        self.update_button.setText(_translate("ConfigMainWindow", "检查更新"))
        self.animation_checkBox.setText(_translate("ConfigMainWindow", "抽取动画"))
        self.groupBox_2.setTitle(_translate("ConfigMainWindow", "高级"))
        self.label.setText(_translate("ConfigMainWindow", "动画时长:"))
        self.ani_time_edit.setText(_translate("ConfigMainWindow", "0"))
        self.label_9.setText(_translate("ConfigMainWindow", "px"))
        self.label_3.setText(_translate("ConfigMainWindow", "多音字播报指定读音(最多三组):"))
        self.label_4.setText(_translate("ConfigMainWindow", "-->"))
        self.label_5.setText(_translate("ConfigMainWindow", "-->"))
        self.label_6.setText(_translate("ConfigMainWindow", "-->"))
        self.label_2.setText(_translate("ConfigMainWindow", "s"))
        self.label_8.setText(_translate("ConfigMainWindow", "悬浮窗大小(重启后生效):"))
        self.floatsize_edit.setText(_translate("ConfigMainWindow", "0"))
        self.label_10.setText(_translate("ConfigMainWindow", "播报语速:"))
        self.speed_edit.setText(_translate("ConfigMainWindow", "0"))
        self.cancel_button.setText(_translate("ConfigMainWindow", "取消"))
        self.save_button.setText(_translate("ConfigMainWindow", "保存"))
        self.label_7.setText(_translate("ConfigMainWindow", "(说明:多音字替换左边填写被替换的名字[e.g.张茜],右边填写替换后读音[e.g.张西]"))

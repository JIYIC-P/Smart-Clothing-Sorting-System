# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1440, 820)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.koutu_img = QtWidgets.QLabel(self.tab)
        self.koutu_img.setGeometry(QtCore.QRect(430, 30, 391, 731))
        self.koutu_img.setObjectName("koutu_img")
        self.img_orign = QtWidgets.QLabel(self.tab)
        self.img_orign.setEnabled(True)
        self.img_orign.setGeometry(QtCore.QRect(10, 10, 401, 751))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_orign.sizePolicy().hasHeightForWidth())
        self.img_orign.setSizePolicy(sizePolicy)
        self.img_orign.setObjectName("img_orign")
        self.choice_push = QtWidgets.QComboBox(self.tab)
        self.choice_push.setGeometry(QtCore.QRect(1010, 250, 131, 31))
        self.choice_push.setObjectName("choice_push")
        self.choice_push.addItem("")
        self.choice_push.addItem("")
        self.choice_push.addItem("")
        self.choice_push.addItem("")
        self.choice_push.addItem("")
        self.float_value = QtWidgets.QTextEdit(self.tab)
        self.float_value.setGeometry(QtCore.QRect(900, 250, 101, 81))
        self.float_value.setObjectName("float_value")
        self.btn_remember = QtWidgets.QPushButton(self.tab)
        self.btn_remember.setGeometry(QtCore.QRect(1010, 280, 131, 51))
        self.btn_remember.setObjectName("btn_remember")
        self.txt_hsv = QtWidgets.QTextEdit(self.tab)
        self.txt_hsv.setGeometry(QtCore.QRect(930, 50, 480, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_hsv.sizePolicy().hasHeightForWidth())
        self.txt_hsv.setSizePolicy(sizePolicy)
        self.txt_hsv.setObjectName("txt_hsv")
        self.btn_reset = QtWidgets.QPushButton(self.tab)
        self.btn_reset.setGeometry(QtCore.QRect(1200, 320, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_reset.sizePolicy().hasHeightForWidth())
        self.btn_reset.setSizePolicy(sizePolicy)
        self.btn_reset.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_reset.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_reset.setObjectName("btn_reset")
        self.btn_start = QtWidgets.QPushButton(self.tab)
        self.btn_start.setGeometry(QtCore.QRect(1200, 250, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy)
        self.btn_start.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_start.setObjectName("btn_start")
        self.comboBox_mode = QtWidgets.QComboBox(self.tab)
        self.comboBox_mode.setGeometry(QtCore.QRect(1200, 390, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_mode.sizePolicy().hasHeightForWidth())
        self.comboBox_mode.setSizePolicy(sizePolicy)
        self.comboBox_mode.setMinimumSize(QtCore.QSize(200, 60))
        self.comboBox_mode.setMaximumSize(QtCore.QSize(100, 60))
        self.comboBox_mode.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.txt_hsv_2 = QtWidgets.QTextEdit(self.tab)
        self.txt_hsv_2.setGeometry(QtCore.QRect(930, 150, 480, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_hsv_2.sizePolicy().hasHeightForWidth())
        self.txt_hsv_2.setSizePolicy(sizePolicy)
        self.txt_hsv_2.setObjectName("txt_hsv_2")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(1140, 110, 90, 30))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(1130, 10, 90, 30))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(910, 220, 90, 30))
        self.label_6.setObjectName("label_6")
        self.btn_motor_color_1 = QtWidgets.QPushButton(self.tab)
        self.btn_motor_color_1.setGeometry(QtCore.QRect(40, 650, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_motor_color_1.sizePolicy().hasHeightForWidth())
        self.btn_motor_color_1.setSizePolicy(sizePolicy)
        self.btn_motor_color_1.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_motor_color_1.setText("")
        self.btn_motor_color_1.setObjectName("btn_motor_color_1")
        self.btn_motor_color_2 = QtWidgets.QPushButton(self.tab)
        self.btn_motor_color_2.setGeometry(QtCore.QRect(260, 650, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_motor_color_2.sizePolicy().hasHeightForWidth())
        self.btn_motor_color_2.setSizePolicy(sizePolicy)
        self.btn_motor_color_2.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_motor_color_2.setText("")
        self.btn_motor_color_2.setObjectName("btn_motor_color_2")
        self.btn_motor_color_3 = QtWidgets.QPushButton(self.tab)
        self.btn_motor_color_3.setGeometry(QtCore.QRect(480, 650, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_motor_color_3.sizePolicy().hasHeightForWidth())
        self.btn_motor_color_3.setSizePolicy(sizePolicy)
        self.btn_motor_color_3.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_motor_color_3.setText("")
        self.btn_motor_color_3.setObjectName("btn_motor_color_3")
        self.btn_motor_color_4 = QtWidgets.QPushButton(self.tab)
        self.btn_motor_color_4.setGeometry(QtCore.QRect(920, 650, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_motor_color_4.sizePolicy().hasHeightForWidth())
        self.btn_motor_color_4.setSizePolicy(sizePolicy)
        self.btn_motor_color_4.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_motor_color_4.setText("")
        self.btn_motor_color_4.setObjectName("btn_motor_color_4")
        self.btn_motor_color_5 = QtWidgets.QPushButton(self.tab)
        self.btn_motor_color_5.setGeometry(QtCore.QRect(700, 650, 200, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_motor_color_5.sizePolicy().hasHeightForWidth())
        self.btn_motor_color_5.setSizePolicy(sizePolicy)
        self.btn_motor_color_5.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_motor_color_5.setText("")
        self.btn_motor_color_5.setObjectName("btn_motor_color_5")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_output = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_output.setObjectName("groupBox_output")
        self.verticalLayout.addWidget(self.groupBox_output)
        self.groupBox_input = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_input.setObjectName("groupBox_input")
        self.verticalLayout.addWidget(self.groupBox_input)
        self.verticalLayout_11.addLayout(self.verticalLayout)
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 28))
        self.label_20.setText("")
        self.label_20.setObjectName("label_20")
        self.verticalLayout_11.addWidget(self.label_20)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 700))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.tab_3)
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 0, 2, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_load = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_load.sizePolicy().hasHeightForWidth())
        self.btn_load.setSizePolicy(sizePolicy)
        self.btn_load.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_load.setObjectName("btn_load")
        self.verticalLayout_2.addWidget(self.btn_load)
        self.btn_add = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout_2.addWidget(self.btn_add)
        self.btn_apply = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_apply.sizePolicy().hasHeightForWidth())
        self.btn_apply.setSizePolicy(sizePolicy)
        self.btn_apply.setMinimumSize(QtCore.QSize(200, 60))
        self.btn_apply.setObjectName("btn_apply")
        self.verticalLayout_2.addWidget(self.btn_apply)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMaximumSize(QtCore.QSize(230, 16777215))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.label_1 = QtWidgets.QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy)
        self.label_1.setObjectName("label_1")
        self.horizontalLayout_2.addWidget(self.label_1)
        self.label = QtWidgets.QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Light = QtWidgets.QLabel(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Light.sizePolicy().hasHeightForWidth())
        self.Light.setSizePolicy(sizePolicy)
        self.Light.setObjectName("Light")
        self.horizontalLayout.addWidget(self.Light)
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(200, 60))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 60))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QtCore.QSize(200, 60))
        self.comboBox_2.setMaximumSize(QtCore.QSize(100, 60))
        self.comboBox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_2)
        self.comboBox_1 = QtWidgets.QComboBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_1.sizePolicy().hasHeightForWidth())
        self.comboBox_1.setSizePolicy(sizePolicy)
        self.comboBox_1.setMinimumSize(QtCore.QSize(200, 60))
        self.comboBox_1.setMaximumSize(QtCore.QSize(100, 60))
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.comboBox_1.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_17 = QtWidgets.QLabel(self.tab_3)
        self.label_17.setText("")
        self.label_17.setObjectName("label_17")
        self.verticalLayout_3.addWidget(self.label_17)
        self.label_18 = QtWidgets.QLabel(self.tab_3)
        self.label_18.setText("")
        self.label_18.setObjectName("label_18")
        self.verticalLayout_3.addWidget(self.label_18)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.gridLayout_5.addLayout(self.verticalLayout_4, 0, 0, 3, 4)
        self.label_16 = QtWidgets.QLabel(self.tab_3)
        self.label_16.setGeometry(QtCore.QRect(40, 360, 277, 16))
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.btn1 = QtWidgets.QPushButton(self.tab_4)
        self.btn1.setGeometry(QtCore.QRect(250, 80, 75, 71))
        self.btn1.setObjectName("btn1")
        self.txt_trg_state = QtWidgets.QTextEdit(self.tab_4)
        self.txt_trg_state.setGeometry(QtCore.QRect(170, 210, 491, 71))
        self.txt_trg_state.setObjectName("txt_trg_state")
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.koutu_img.setText(_translate("Dialog", "img"))
        self.img_orign.setText(_translate("Dialog", "test"))
        self.choice_push.setItemText(0, _translate("Dialog", "推杆1"))
        self.choice_push.setItemText(1, _translate("Dialog", "推杆2"))
        self.choice_push.setItemText(2, _translate("Dialog", "推杆3"))
        self.choice_push.setItemText(3, _translate("Dialog", "推杆4"))
        self.choice_push.setItemText(4, _translate("Dialog", "推杆5"))
        self.btn_remember.setText(_translate("Dialog", "应用"))
        self.btn_reset.setText(_translate("Dialog", "重置"))
        self.btn_start.setText(_translate("Dialog", "开始"))
        self.comboBox_mode.setItemText(0, _translate("Dialog", "颜色"))
        self.comboBox_mode.setItemText(1, _translate("Dialog", "白浅深"))
        self.comboBox_mode.setItemText(2, _translate("Dialog", "形状"))
        self.label_2.setText(_translate("Dialog", "衣服"))
        self.label_4.setText(_translate("Dialog", "当前值"))
        self.label_6.setText(_translate("Dialog", "偏移量"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Tab 1"))
        self.groupBox_output.setTitle(_translate("Dialog", "GroupBox"))
        self.groupBox_input.setTitle(_translate("Dialog", "GroupBox"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))
        self.btn_load.setText(_translate("Dialog", "加载设置"))
        self.btn_add.setText(_translate("Dialog", "添加一行"))
        self.btn_apply.setText(_translate("Dialog", "应用"))
        self.label_1.setText(_translate("Dialog", "波特率"))
        self.label.setText(_translate("Dialog", "串口选择"))
        self.Light.setText(_translate("Dialog", "TextLabel"))
        self.pushButton.setText(_translate("Dialog", "连接"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "38400"))
        self.comboBox_1.setItemText(0, _translate("Dialog", "COM3"))
        self.comboBox_1.setItemText(1, _translate("Dialog", "COM4"))
        self.comboBox_1.setItemText(2, _translate("Dialog", "COM1"))
        self.comboBox_1.setItemText(3, _translate("Dialog", "COM2"))
        self.comboBox_1.setItemText(4, _translate("Dialog", "COM5"))
        self.comboBox_1.setItemText(5, _translate("Dialog", "COM6"))
        self.comboBox_1.setItemText(6, _translate("Dialog", "COM7"))
        self.comboBox_1.setItemText(7, _translate("Dialog", "COM8"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Tab3"))
        self.btn1.setText(_translate("Dialog", "bbb"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "页"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\rs232Skeleton.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(577, 495)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.paramVerticalLayout = QtWidgets.QVBoxLayout()
        self.paramVerticalLayout.setObjectName("paramVerticalLayout")
        self.paramLayout = QtWidgets.QHBoxLayout()
        self.paramLayout.setObjectName("paramLayout")
        self.portName = QtWidgets.QLineEdit(Form)
        self.portName.setObjectName("portName")
        self.paramLayout.addWidget(self.portName)
        self.baudrateSpinbox = QtWidgets.QSpinBox(Form)
        self.baudrateSpinbox.setMaximum(30000000)
        self.baudrateSpinbox.setProperty("value", 1200)
        self.baudrateSpinbox.setObjectName("baudrateSpinbox")
        self.paramLayout.addWidget(self.baudrateSpinbox)
        self.bytesizeSpinbox = QtWidgets.QSpinBox(Form)
        self.bytesizeSpinbox.setPrefix("")
        self.bytesizeSpinbox.setMinimum(5)
        self.bytesizeSpinbox.setMaximum(8)
        self.bytesizeSpinbox.setProperty("value", 7)
        self.bytesizeSpinbox.setObjectName("bytesizeSpinbox")
        self.paramLayout.addWidget(self.bytesizeSpinbox)
        self.stopBitsSpinBox = QtWidgets.QDoubleSpinBox(Form)
        self.stopBitsSpinBox.setDecimals(1)
        self.stopBitsSpinBox.setMinimum(1.0)
        self.stopBitsSpinBox.setMaximum(2.0)
        self.stopBitsSpinBox.setSingleStep(0.5)
        self.stopBitsSpinBox.setObjectName("stopBitsSpinBox")
        self.paramLayout.addWidget(self.stopBitsSpinBox)
        self.parityComboBox = QtWidgets.QComboBox(Form)
        self.parityComboBox.setObjectName("parityComboBox")
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.parityComboBox.addItem("")
        self.paramLayout.addWidget(self.parityComboBox)
        self.paramVerticalLayout.addLayout(self.paramLayout)
        self.flowControlLayout = QtWidgets.QHBoxLayout()
        self.flowControlLayout.setObjectName("flowControlLayout")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.flowControlLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(Form)
        self.checkBox_2.setObjectName("checkBox_2")
        self.flowControlLayout.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(Form)
        self.checkBox_3.setObjectName("checkBox_3")
        self.flowControlLayout.addWidget(self.checkBox_3)
        self.paramVerticalLayout.addLayout(self.flowControlLayout)
        self.verticalLayout.addLayout(self.paramVerticalLayout)
        self.outputText = QtWidgets.QPlainTextEdit(Form)
        self.outputText.setReadOnly(True)
        self.outputText.setObjectName("outputText")
        self.verticalLayout.addWidget(self.outputText)
        self.sendCommandLayout = QtWidgets.QHBoxLayout()
        self.sendCommandLayout.setObjectName("sendCommandLayout")
        self.commandEdit = QtWidgets.QLineEdit(Form)
        self.commandEdit.setObjectName("commandEdit")
        self.sendCommandLayout.addWidget(self.commandEdit)
        self.commandSendButton = QtWidgets.QPushButton(Form)
        self.commandSendButton.setObjectName("commandSendButton")
        self.sendCommandLayout.addWidget(self.commandSendButton)
        self.verticalLayout.addLayout(self.sendCommandLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.connectionLayout = QtWidgets.QVBoxLayout()
        self.connectionLayout.setObjectName("connectionLayout")
        self.connectButton = QtWidgets.QPushButton(Form)
        self.connectButton.setObjectName("connectButton")
        self.connectionLayout.addWidget(self.connectButton)
        self.disconnectButton = QtWidgets.QPushButton(Form)
        self.disconnectButton.setObjectName("disconnectButton")
        self.connectionLayout.addWidget(self.disconnectButton)
        self.verticalLayout_2.addLayout(self.connectionLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 98, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.toolsLayout = QtWidgets.QVBoxLayout()
        self.toolsLayout.setObjectName("toolsLayout")
        self.saveOutputButton = QtWidgets.QPushButton(Form)
        self.saveOutputButton.setObjectName("saveOutputButton")
        self.toolsLayout.addWidget(self.saveOutputButton)
        self.exportCSVButton = QtWidgets.QPushButton(Form)
        self.exportCSVButton.setObjectName("exportCSVButton")

        # Save mWave file Yolo Bitch
        self.exportMWaveButton = QtWidgets.QPushButton(Form)
        self.exportMWaveButton.setObjectName("exportMWaveButton")
        # --> Finish save_mWaveFile

        self.toolsLayout.addWidget(self.exportCSVButton)
        self.toolsLayout.addWidget(self.exportMWaveButton)

        self.plotButton = QtWidgets.QPushButton(Form)
        self.plotButton.setObjectName("plotButton")
        self.toolsLayout.addWidget(self.plotButton)
        self.verticalLayout_2.addLayout(self.toolsLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        Form.setToolTip(_translate("Form", "Enable hardware (DSR/DTR) flow control."))
        self.portName.setToolTip(_translate("Form", "Device name or port number number"))
        self.portName.setText(_translate("Form", "COM3"))
        self.baudrateSpinbox.setToolTip(_translate("Form", " Baud rate such as 9600 or 115200 etc"))
        self.bytesizeSpinbox.setToolTip(
            _translate("Form", "Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS"))
        self.bytesizeSpinbox.setSuffix(_translate("Form", " bits"))
        self.stopBitsSpinBox.setToolTip(_translate("Form",
                                                   "Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO"))
        self.parityComboBox.setItemText(0, _translate("Form", "Odd"))
        self.parityComboBox.setItemText(1, _translate("Form", "Even"))
        self.parityComboBox.setItemText(2, _translate("Form", "None"))
        self.checkBox.setToolTip(_translate("Form", "Enable software flow control."))
        self.checkBox.setText(_translate("Form", "xonxoff"))
        self.checkBox_2.setToolTip(_translate("Form", "Enable hardware (RTS/CTS) flow control."))
        self.checkBox_2.setText(_translate("Form", "rtscts"))
        self.checkBox_3.setToolTip(_translate("Form", "Enable hardware (DSR/DTR) flow control."))
        self.checkBox_3.setText(_translate("Form", "dsrdtr"))
        self.commandSendButton.setText(_translate("Form", "Send"))
        self.connectButton.setText(_translate("Form", "Connect"))
        self.disconnectButton.setText(_translate("Form", "Disconnect"))
        self.saveOutputButton.setText(_translate("Form", "Save Output"))

        # SAVE mWave Button
        self.exportMWaveButton.setText(_translate("Form", "Export to MWave"))

        self.exportCSVButton.setText(_translate("Form", "Export to CSV"))
        self.plotButton.setText(_translate("Form", "Plot "))

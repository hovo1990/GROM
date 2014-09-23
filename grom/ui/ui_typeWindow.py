# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'type_qt5.ui'
#
# Created: Tue Sep 23 23:15:28 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fileType(object):
    def setupUi(self, fileType):
        fileType.setObjectName("fileType")
        fileType.resize(388, 200)
        fileType.setMinimumSize(QtCore.QSize(388, 200))
        fileType.setMaximumSize(QtCore.QSize(390, 200))
        self.gridLayout = QtWidgets.QGridLayout(fileType)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ParamButton = QtWidgets.QRadioButton(fileType)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.ParamButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/settings-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ParamButton.setIcon(icon)
        self.ParamButton.setIconSize(QtCore.QSize(40, 40))
        self.ParamButton.setObjectName("ParamButton")
        self.verticalLayout.addWidget(self.ParamButton)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.CoordButton = QtWidgets.QRadioButton(fileType)
        self.CoordButton.setMaximumSize(QtCore.QSize(280, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.CoordButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/xyz.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CoordButton.setIcon(icon1)
        self.CoordButton.setIconSize(QtCore.QSize(40, 40))
        self.CoordButton.setObjectName("CoordButton")
        self.verticalLayout.addWidget(self.CoordButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 22, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.groupModelType = QtWidgets.QGroupBox(fileType)
        self.groupModelType.setMinimumSize(QtCore.QSize(120, 91))
        self.groupModelType.setAutoFillBackground(False)
        self.groupModelType.setFlat(False)
        self.groupModelType.setCheckable(False)
        self.groupModelType.setObjectName("groupModelType")
        self.widget = QtWidgets.QWidget(self.groupModelType)
        self.widget.setGeometry(QtCore.QRect(0, 20, 112, 71))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pdbButton = QtWidgets.QRadioButton(self.widget)
        self.pdbButton.setObjectName("pdbButton")
        self.verticalLayout_2.addWidget(self.pdbButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 22, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.groButton = QtWidgets.QRadioButton(self.widget)
        self.groButton.setObjectName("groButton")
        self.verticalLayout_2.addWidget(self.groButton)
        self.verticalLayout_3.addWidget(self.groupModelType)
        spacerItem4 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(fileType)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(fileType)
        QtCore.QMetaObject.connectSlotsByName(fileType)

    def retranslateUi(self, fileType):
        _translate = QtCore.QCoreApplication.translate
        fileType.setWindowTitle(_translate("fileType", "File Type"))
        self.ParamButton.setText(_translate("fileType", "Param File"))
        self.CoordButton.setText(_translate("fileType", "Coordinate File"))
        self.groupModelType.setTitle(_translate("fileType", "Model Type:"))
        self.pdbButton.setText(_translate("fileType", "pdb Format"))
        self.groButton.setText(_translate("fileType", "gro Format"))

import type_rc

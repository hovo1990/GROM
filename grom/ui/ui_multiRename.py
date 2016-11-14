# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_multi_rename_qt5.ui'
#
# Created: Thu Aug 14 17:13:08 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Multi_Rename_Dialog(object):
    def setupUi(self, Multi_Rename_Dialog):
        Multi_Rename_Dialog.setObjectName("Multi_Rename_Dialog")
        Multi_Rename_Dialog.resize(194, 105)
        Multi_Rename_Dialog.setMinimumSize(QtCore.QSize(194, 105))
        Multi_Rename_Dialog.setMaximumSize(QtCore.QSize(300, 150))
        self.gridLayout = QtWidgets.QGridLayout(Multi_Rename_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.RenamebuttonBox = QtWidgets.QDialogButtonBox(Multi_Rename_Dialog)
        self.RenamebuttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.RenamebuttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.RenamebuttonBox.setObjectName("RenamebuttonBox")
        self.gridLayout.addWidget(self.RenamebuttonBox, 2, 0, 1, 1)
        self.RnameLabel = QtWidgets.QLabel(Multi_Rename_Dialog)
        self.RnameLabel.setObjectName("RnameLabel")
        self.gridLayout.addWidget(self.RnameLabel, 0, 0, 1, 1)
        self.RenamelineEdit = QtWidgets.QLineEdit(Multi_Rename_Dialog)
        self.RenamelineEdit.setObjectName("RenamelineEdit")
        self.gridLayout.addWidget(self.RenamelineEdit, 1, 0, 1, 1)

        self.retranslateUi(Multi_Rename_Dialog)
        self.RenamebuttonBox.accepted.connect(Multi_Rename_Dialog.accept)
        self.RenamebuttonBox.rejected.connect(Multi_Rename_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Multi_Rename_Dialog)

    def retranslateUi(self, Multi_Rename_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Multi_Rename_Dialog.setWindowTitle(_translate("Multi_Rename_Dialog", "Dialog"))
        self.RnameLabel.setText(_translate("Multi_Rename_Dialog", "Rename to:"))

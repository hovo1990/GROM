# -*- coding: utf-8 -*-
"""
    GROM modules
    ~~~~~~~~~~~~

    Implements help browser widget,

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""

#: Importing from  PyQt5.QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox

#: Importing from  PyQt5.QtWebKitWidgets
from  PyQt5.QtWebKitWidgets import QWebView

from ui import ui_multiRename as MR
from ui import ui_typeWindow as TW


class Browser(QWebView):
    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        print(str(frame.toHtml()).encode('utf-8'))


class MultipleRenameDialog(QDialog, MR.Ui_Multi_Rename_Dialog):  # Need to fix these

    def __init__(self, parent=None):
        super(MultipleRenameDialog, self).__init__(parent)
        self.setupUi(self)
        # self.ParamButton.setChecked(True)
        # self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        # self.connect(self.ParamButton, SIGNAL('clicked()'), self.update)
        # self.connect(self.CoordButton, SIGNAL('clicked()'), self.update)

        # self.buttonBox.accepted.connect(self.accept) #This way it works right !!! :D
        # self.buttonBox.rejected.connect(self.reject)

        # def update(self):
        # self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)


class ChooseDialog(QDialog, TW.Ui_fileType):
    def __init__(self, parent=None):
        super(ChooseDialog, self).__init__(parent)
        self.setupUi(self)
        # self.ParamButton.setChecked(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.groupModelType.setDisabled(True)

        self.ParamButton.clicked.connect(self.update)
        # self.ParamButton.clicked.connect(self.deactivateModelButtons)
        self.CoordButton.clicked.connect(self.disableBox)
        self.CoordButton.clicked.connect(self.updateModelButtons)

        self.pdbButton.clicked.connect(self.update)
        self.groButton.clicked.connect(self.update)

        self.CoordButton.clicked.connect(self.enableModelType)
        self.ParamButton.clicked.connect(self.disableModelType)

        self.buttonBox.accepted.connect(self.accept)  # This way it works right !!! :D
        self.buttonBox.rejected.connect(self.reject)

    def disableBox(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

    def update(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)

    def enableModelType(self):
        self.groupModelType.setDisabled(False)

    def disableModelType(self):
        self.groupModelType.setDisabled(True)

    def updateModelButtons(self):
        if self.pdbButton.isChecked():
            self.update()
        elif self.groButton.isChecked():
            self.update()

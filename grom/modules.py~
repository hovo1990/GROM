# -*- coding: utf-8 -*-
"""
    GROM modules
    ~~~~~~~~~~~~

    Implements help browser widget,

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""


from PyQt5.QtWidgets import (QDialog,QDialogButtonBox )
from  PyQt5.QtWebKitWidgets import (QWebView)
import ui_multiRename as MR #This is new
import ui_typeWindow as TW #Adding New Stuff for New File


class Browser(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        print(unicode(frame.toHtml()).encode('utf-8'))


class MultipleRenameDialog(QDialog, MR.Ui_Multi_Rename_Dialog): #Need to fix these

    def __init__(self,parent = None):
        super(MultipleRenameDialog, self).__init__(parent)
        self.setupUi(self)
        #self.ParamButton.setChecked(True)
        #self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        #self.connect(self.ParamButton, SIGNAL('clicked()'), self.update)
        #self.connect(self.CoordButton, SIGNAL('clicked()'), self.update)

        #self.buttonBox.accepted.connect(self.accept) #This way it works right !!! :D
        #self.buttonBox.rejected.connect(self.reject)

    #def update(self):
        #self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)


class ChooseDialog(QDialog, TW.Ui_fileType):

    def __init__(self,parent = None):
        super(ChooseDialog, self).__init__(parent)
        self.setupUi(self)
        #self.ParamButton.setChecked(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        self.ParamButton.clicked.connect(self.update)
        self.CoordButton.clicked.connect(self.update)



        self.buttonBox.accepted.connect(self.accept) #This way it works right !!! :D
        self.buttonBox.rejected.connect(self.reject)

    def update(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
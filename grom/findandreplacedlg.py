# -*- coding: utf-8 -*-
"""
    GROM.findandreplacedlg
    ~~~~~~~~~~~~~

    Implements find and replace dialog

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""


import re
import sys
from PyQt5.QtCore import  (Qt )
#from PyQt5.QtGui import  (QTextCharFormat)
from PyQt5.QtWidgets import (QDialog, QTextEdit)
sys.path.append('ui/')
import ui.ui_findReplace as ui_findReplace
import Icons_rc

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False


class FindAndReplaceDlg(QDialog,
        ui_findReplace.Ui_FindAndReplaceDlg):

    showFrame = False

    def __init__(self,state ='search', table = None, text = None, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)
        self.__text = str(text)

        self.state = state
        self.__table = table #Careful Here
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(300,200)
        self.setAttribute(Qt.WA_DeleteOnClose)
        if not MAC:
            self.findButton.setFocusPolicy(Qt.NoFocus)
            self.replaceButton.setFocusPolicy(Qt.NoFocus)
            self.replaceAllButton.setFocusPolicy(Qt.NoFocus)
            self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.updateUi() #VIT

        #: hides several widgets,since code hasn't been implemented yet
        self.hideObjects()



        #: --> sets Up signals
        self.findButton.clicked.connect(self.findAll)
        self.findLineEdit.textChanged.connect(self.search)
        self.replaceLineEdit.textChanged.connect(self.changeReplaceValue)
        self.DownSearch.clicked.connect(self.downSearch)
        self.UpSearch.clicked.connect(self.upSearch)
        self.replaceButton.clicked.connect(self.replaceButton_clicked)
        self.replaceAllButton.clicked.connect(self.replaceAllButton_clicked)
        #: Signals End





    def hideObjects(self):
        """
        Methods hides widgets because code hasn't been implemented yet
        """
        self.frameCoord.hide()
        self.CoordOptionsButton.hide()
        self.caseCheckBox.hide()
        self.wholeCheckBox.hide()
        self.syntaxComboBox.hide()
        self.label_3.hide()
        self.CoordOptionsButton.setEnabled(False)


    def changeFindValue(self):
        self.searchVal = str(self.findLineEdit.text())
        self.currenWidget.setSearchTextValue(self.searchVal,self.replaceVal)

    def changeReplaceValue(self):
        self.replaceVal = str(self.replaceLineEdit.text())
        self.currenWidget.setSearchTextValue(self.searchVal,self.replaceVal)


    def upSearch(self):
        """
        Method for searching by going up the content
        """
        self.currenWidget.upMove()

    def downSearch(self):
        """
        Method for searching by going down the content
        """
        self.currenWidget.downMove()

    def on_findLineEdit_textEdited(self, text):
        self.__index = 0
        self.updateUi()



    def fillFields(self,searchVal = '',replaceVal = ''):
        """
        Method to fill the fields for Find and Replace Dialog

        Args:
             searchVal (str):  Value for Search Field in Dialog
             replaceVal (str): Value for Replace Field in Dialog

        """
        self.searchVal = searchVal
        self.replaceVal = replaceVal
        self.findLineEdit.setText(self.searchVal)
        self.replaceLineEdit.setText(self.replaceVal) #Here is the problem
        self.updateUi() #VIT

    def AddInfo(self,currentWidget = None):
        """
        Method to update active Widget reference and set Up Dialog according
        to its instance, whether it's a TextEditor or TableEditr

        Args:
             currentWidget (QWidget*): Address of the Widget
        """
        self.currenWidget = currentWidget
        if self.currenWidget is None:
            pass
        elif  isinstance(self.currenWidget, QTextEdit):
            self.findButton.hide()
            self.CoordOptionsButton.setEnabled(False)
            self.frameCoord.hide()
        else:
            self.findButton.show()
            self.CoordOptionsButton.setEnabled(True)
        try:
            values = self.currenWidget.getSearchTextValue()
            #:Fills Dialog Fields with Values
            self.fillFields(values[0],values[1])
        except:
            pass





    def replaceButton_clicked(self):
        """
        Method to replace Item with specified Value
        """
        self.replaceVal = str(self.replaceLineEdit.text())
        self.syntaxCombo = str(self.syntaxComboBox.currentText())
        self.currenWidget.replace(self.replaceVal,self.syntaxCombo)



    def replaceAllButton_clicked(self):
        """
        Method to replace all Item with specified Value
        """
        self.searchVal = str(self.findLineEdit.text())
        self.replaceVal = str(self.replaceLineEdit.text())
        self.syntaxCombo = str(self.syntaxComboBox.currentText())
        self.currenWidget.replaceAll(self.searchVal,self.replaceVal)


    def search(self):
        """
        Method to dynamically change Search Result for TextEditor or
        change initial row and column to start Search for TableEditor
        """
        try:
            self.syntaxCombo = str(self.syntaxComboBox.currentText())
            self.searchVal = str(self.findLineEdit.text())
            self.replaceVal = str(self.replaceLineEdit.text())
            self.currenWidget.search(self.searchVal,self.replaceVal,self.syntaxCombo)
        except:
            self.currenWidget.updateToZero()


    def findAll(self):
        """
        Method to find all items in table Widget
        """
        try:
            self.searchVal = str(self.findLineEdit.text())
            self.currenWidget.findAll(self.searchVal)
        except Exception as error:
            print("Error: ",error)

    def updateUi(self):
        """
        Method that checks length of findLineedit and enables Buttons
        """
        enable = not len(self.findLineEdit.text()) <1 #need to fix this
        self.DownSearch.setEnabled(enable)
        self.UpSearch.setEnabled(enable)
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)


    #: ---> This methods are for a future release
    def deactivateCoordChecks(self):
        self.checkBoxAtom.setChecked(False)
        self.checkBoxSerial.setChecked(False)
        self.checkBoxName.setChecked(False)
        self.checkBoxResName.setChecked(False)
        self.checkBoxChainID.setChecked(False)
        self.checkBoxResSeq.setChecked(False)
        self.checkBoxX.setChecked(False)
        self.checkBoxY.setChecked(False)
        self.checkBoxZ.setChecked(False)
        self.checkBoxOccup.setChecked(False)
        self.checkBoxTempFact.setChecked(False)
        self.checkBoxElem.setChecked(False)

    def activateCoordChecks(self):
        self.checkBoxAtom.setChecked(True)
        self.checkBoxSerial.setChecked(True)
        self.checkBoxName.setChecked(True)
        self.checkBoxResName.setChecked(True)
        self.checkBoxChainID.setChecked(True)
        self.checkBoxResSeq.setChecked(True)
        self.checkBoxX.setChecked(True)
        self.checkBoxY.setChecked(True)
        self.checkBoxZ.setChecked(True)
        self.checkBoxOccup.setChecked(True)
        self.checkBoxTempFact.setChecked(True)
        self.checkBoxElem.setChecked(True)



    def activateFrame(self): #!!!!!!!
        self.resize(200,200)
        if self.showFrame == False:
            self.frameCoord.show()
            self.showFrame = True
        else:
            self.showFrame = False
            self.frameCoord.hide()

    #: ---> END




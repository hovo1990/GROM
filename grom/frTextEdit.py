# -*- coding: utf-8 -*-
"""
    GROM.frTextEdit
    ~~~~~~~~~~~~~

    This is  Search Object for Text Editor Widget

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

import re
#from PyQt5.QtCore import *
from PyQt5.QtGui import  (QBrush, QColor, QTextCharFormat, QTextCursor)
from PyQt5.QtWidgets import (QTextEdit)

try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str


class frTextObject():

    def __init__(self,textEditorAddress,parent = None):
        """
        Method defines  Search Object for Text Editor Widget

        Args:
             textEditorAddress (QWidget*) Reference Address for Text Editor
        """
        #super(frTextObject, self).__init__(parent)
        self.__textEditor = textEditorAddress
        self.__text = self.__textEditor.toPlainText()
        print('textEditorAddress is ',self.__textEditor)



        self.__findText = ''
        self.__replaceText = ''


        self.found = False
        self.__index = 0

        self.resPTRdown = 0
        self.resPTRup = 0
        self.resFoundText = []
        self.resSelected = []


    def setFindVal(self,val1,val2):
        self.__findText = val1
        self.__replaceText = val2

    def getFindText(self):
        return [self.__findText,self.__replaceText]


    def updateTextContent(self):
        self.__text = self.__textEditor.toPlainText()

    def getText(self):
        print('text is  come on',self.textEditorAddress.toPlainText())


    def makeRegex(self,findText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        if syntaxCombo == "Literal":
            findText = re.escape(findText)
        flags = re.MULTILINE|re.DOTALL|re.UNICODE
        if not caseCheckBox:
            flags |= re.IGNORECASE
        if wholeCheckBox:
            findText = r"\b{0}\b".format(findText)
        return re.compile(findText, flags)



    def replace(self,replaceText,syntaxCombo):
        try:
            self.__replaceText = replaceText
            print('fuck fuck fuck ',replaceText)
            self.cursor.removeSelectedText()
            self.cursor.insertText(replaceText)
            self.search(self.__findText,syntaxCombo)
            self.fixResFindValues()
        except:
            print("something  didn't work with replace")


    def replaceAll(self,findText,replaceText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        try:
            self.__replaceText = replaceText
            regex = self.makeRegex(findText,syntaxCombo)
            self.__text = regex.sub(replaceText,
                                    self.__text)
            self.__textEditor.setText(self.__text)
            self.fixFormat(self.__textEditor)
        except:
            print("something  didn't work with replace all")

    def fixFormat(self):
        try:
            cursor_clear = self.__textEditor.textCursor()
            format_clear = QTextCharFormat()
            format_clear.setBackground(QBrush(QColor(30, 30, 30)))
            cursor_clear.setPosition(0)
            cursor_clear.movePosition(QTextCursor.End,QTextCursor.KeepAnchor)
            cursor_clear.mergeCharFormat(format_clear)
        except:
            print("something  didn't work with fixFormat")

    def cursorMove(self,start,end):
        try:
            self.cursor = self.__textEditor.textCursor()
            self.cursor.setPosition(start)
            to_move = end-start
            self.cursor.movePosition(QTextCursor.NextCharacter,QTextCursor.KeepAnchor ,to_move)
            self.__textEditor.setFocus()
            self.__textEditor.setTextCursor(self.cursor)
        except:
            print("something  didn't work with cursorMove")

    def fixResFindValues(self):
        self.resPTRup -= 2
        self.resPTRdown -= 1
        self.resPTRup = self.resPTRdown - 2
        if self.resPTRdown == len(self.resFoundText):
            self.resPTRdown = 0
        if self.resPTRup < 0:
            self.resPTRup = len(self.resFoundText) -1
            self.resPTRdown = 0

    def upSearch(self):
        try:
            self.__textEditor.ensureCursorVisible()
            start = self.resFoundText[self.resPTRup][0]
            end = self.resFoundText[self.resPTRup][1]
            print('start is %s end is %s'%(start,end))
            self.cursorMove(start,end)
            self.resSelected = [start,end]
            self.resPTRup -= 1
            self.resPTRdown = self.resPTRup + 2
            if self.resPTRup < 0:
                self.resPTRup = len(self.resFoundText) -1
                self.resPTRdown = 0
        except:
            print("Duh Up search")


    def downSearch(self):
        try:
            start = self.resFoundText[self.resPTRdown][0]
            self.__textEditor.ensureCursorVisible()
            end = self.resFoundText[self.resPTRdown][1]
            self.resSelected = [start,end]
            self.cursorMove(start,end)
            self.resPTRdown += 1
            self.resPTRup = self.resPTRdown - 2
            if self.resPTRdown == len(self.resFoundText):
                self.resPTRdown = 0
        except:
            print("Duh down search")

    def search(self,findText,replaceText = None,syntaxCombo = None):
        if self.found  == True:
            self.fixFormat()
        self.__index = 0
        self.__findText = findText
        self.resFoundText = []
        findText = findText
        if len(findText) < 1:
            self.fixFormat()
        else:
            regex = self.makeRegex(findText,syntaxCombo)
            while True:
                match = regex.search(self.__text, self.__index)                  # look here
                if match is  None:
                    self.found = True
                    break
                else:
                    #print("Match is tada",match)
                    self.resFoundText.append([match.start(),match.end()])
                    self.__index = match.end()
                    self.highlightText(findText,match.start())
        self.returnToStart()

    def returnToStart(self):
        cursor = self.__textEditor.textCursor()
        cursor.setPosition(0)
        self.__textEditor.setFocus()
        self.__textEditor.setTextCursor(cursor)

    def highlightText(self,findText,where):
        cursor = self.__textEditor.textCursor()
        format = QTextCharFormat()
        format.setBackground(QBrush(QColor("cyan")))
        cursor.setPosition(where)
        findText = len(findText)
        cursor.movePosition(QTextCursor.NextCharacter,QTextCursor.KeepAnchor ,findText)
        cursor.mergeCharFormat(format)
        self.__textEditor.setFocus()
        self.__textEditor.setTextCursor(cursor)


# -*- coding: utf-8 -*-
"""
    GROM.frTextEdit
    ~~~~~~~~~~~~~

    This is  Search Object for Text Editor Widget

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

import re
#: Importing from PyQt5.QtGui
from PyQt5.QtGui import  QBrush
from PyQt5.QtGui import  QTextFormat
from PyQt5.QtGui import  QColor
from PyQt5.QtGui import  QTextCharFormat
from PyQt5.QtGui import  QTextCursor
from PyQt5.QtGui import  QTextDocument


#: Importing from PyQt5.QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QTextEdit



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
        self.selectedText = False
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
            if self.selectedText == True:
                self.__replaceText = replaceText
                self.cursor.beginEditBlock() #Very IMportant
                self.cursor.removeSelectedText()
                self.cursor.insertText(replaceText)
                self.cursor.endEditBlock() #Very IMportant
                self.search(self.__findText,syntaxCombo)
                self.fixResFindValues()
                self.selectedText = False
        except:
            print("something  didn't work with replace")


    def replaceAll(self,findText,replaceText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        try:
            # Here I am just getting the replacement data
            # from my UI so it will be different for you

            old=findText
            print('old is ',old)
            new=replaceText
            print('new is ',new)

            # Beginning of undo block
            cursor=self.__textEditor.textCursor()
            cursor.beginEditBlock()

            # Use flags for case match
            flags=QTextDocument.FindFlags()
            if caseCheckBox:
                flags=flags|QTextDocument.FindCaseSensitively

            # Replace all we can
            while True:
                # self.editor is the QPlainTextEdit
                r=self.__textEditor.find(old,flags)
                if r:
                    qc=self.__textEditor.textCursor()
                    if qc.hasSelection():
                        qc.insertText(new)
                else:
                    break

            # Mark end of undo block
            cursor.endEditBlock()
            self.search(self.__findText,syntaxCombo)
            self.fixResFindValues()
            self.selectedText = False
            #self.fixFormat()
        except Exception as e:
            print("something  didn't work with replace all: ",e)

    def fixFormat(self):
        try:
            cursor_clear = self.__textEditor.textCursor()
            format_clear = QTextCharFormat()
            format_clear.setBackground(QBrush(QColor(30, 30, 30)))
            cursor_clear.setPosition(0)
            cursor_clear.movePosition(QTextCursor.End,QTextCursor.KeepAnchor)
            cursor_clear.mergeCharFormat(format_clear)
        except Exception as e:
            print("something  didn't work with fixFormat: ",e)

    def cursorMove(self,start,end):
        try:
            self.cursor = self.__textEditor.textCursor()
            self.cursor.setPosition(start)
            to_move = end-start
            self.cursor.movePosition(QTextCursor.NextCharacter,QTextCursor.KeepAnchor ,to_move)
            self.__textEditor.setFocus()
            self.__textEditor.setTextCursor(self.cursor)
            self.selectedText = True
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
        self.extraSelections = self.__textEditor.extraSelections
        self.extraSelections[1] = []
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
            self.__textEditor.document().setModified(False)


        extra = self.extraSelections[0] + self.extraSelections[1]
        self.__textEditor.setExtraSelections(extra)
        #self.returnToStart()



    def highlightText(self,findText,where):
        cursor = self.__textEditor.textCursor()
        #cursor.beginEditBlock() #Very IMportant
        #format = QTextCharFormat()
        #format.setBackground(QBrush(QColor("cyan")))
        cursor.setPosition(where)
        findText = len(findText)
        cursor.movePosition(QTextCursor.NextCharacter,QTextCursor.KeepAnchor ,findText)
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QBrush(QColor("cyan")))
        #selection.format.setProperty(QTextFormat.BackgroundBrush,True)
        selection.cursor = cursor
        #selection.cursor.clearSelection()
        self.extraSelections[1].append(selection)
        #cursor.endEditBlock() #Very IMportant

    def returnToStart(self):
        cursor = self.__textEditor.textCursor()
        cursor.setPosition(0)
        self.__textEditor.setFocus()
        self.__textEditor.setTextCursor(cursor)
        self.__textEditor.document().setModified(False)


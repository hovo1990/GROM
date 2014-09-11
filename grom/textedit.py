# -*- coding: utf-8 -*-
"""
    GROM.textedit
    ~~~~~~~~~~~~~

    This is the main program with its GUI

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""


from PyQt5.QtCore import (Qt,QFile, QFileInfo, QIODevice, QTextStream)
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QTextEdit,QFileDialog)

try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str

import GROMHighlight
import frTextEdit



class TextEdit(QTextEdit):

    NextId = 1

    FONT_MAX_SIZE = 40
    FONT_MIN_SIZE = 1

    def __init__(self, filename= None, parent=None):
        """
        Creates an Instance of QTextEdit

         Args:
             filename (str): for opening a parameter file
             parent  (object)

        """
        super(TextEdit, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.filename = filename
        print('self.filename is ---->>>> ',self.filename)
        if self.filename == None:
            self.filename = QString("Unnamed-{0}.mdp".format(
                                    TextEdit.NextId))
            TextEdit.NextId += 1
        self.document().setModified(False)
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        font = QFont("Courier", 11)
        self.document().setDefaultFont(font)
        self.setFont(font)
        self.setAutoFillBackground(False)
        self.setStyleSheet("QTextEdit { background-color: rgb(30, 30, 30); color: rgb(154, 190, 154);}")

        #: Creates Syntax Highlighter and Find Replace Object for current Widget
        self.highlighter = GROMHighlight.GROMHighlighter(self)
        self.frTextObject = frTextEdit.frTextObject(self)

        #: ---> Signals Start
        self.textChanged.connect(self.updateSearchText)

        self.modificationChanged.connect(self.checkChange)
        self.cursorPositionChanged.connect(self.CursorPosition)
        #: ---> Signals End


    def checkChange(self):
        print('blah blah')

    def zoom_in(self):
        font = self.document().defaultFont()
        size = font.pointSize()
        if size < self.FONT_MAX_SIZE:
            size += 2
            font.setPointSize(size)
        self.setFont(font)


    def zoom_out(self):
        font = self.document().defaultFont()
        size = font.pointSize()
        if size > self.FONT_MIN_SIZE:
            size -= 2
            font.setPointSize(size)
        self.setFont(font)

    def setSearchTextValue(self,val1,val2):
        self.frTextObject.setFindVal(val1,val2)

    def getSearchTextValue(self):
        return  self.frTextObject.getFindText()

    def upMove(self):
        self.frTextObject.upSearch()

    def downMove(self):
        self.frTextObject.downSearch()


    def updateSearchText(self):
        """
        Method for updating findLineEdit
        """
        #print('color changed')
        self.frTextObject.updateTextContent()

    def search(self,findText,replaceText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        """
        Method for searching

        Args:
             findText (str): find Value
             replaceText (str): replace Value
             Rest of the arguments not implemented yet

        """
        self.frTextObject.search(findText,replaceText,syntaxCombo)

    def replace(self,replaceText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        """
        Method responsible with Replacing value

        Args:
             replaceText (str): replace Value

        """
        self.frTextObject.replace(replaceText,syntaxCombo)

    def replaceAll(self,findText,replaceAllText,syntaxCombo = None,caseCheckBox = False,wholeCheckBox = False):
        """
        Method responsible with Replacing all values

        Args:
             replaceAllText (str): replace All with this value
        """
        self.frTextObject.replaceAll(replaceAllText)


    def closeEvent(self, event):
        if (self.document().isModified() and
            QMessageBox.question(self,
                   "G.R.O.M. Editor- Unsaved Changes",
                   "Save unsaved changes in {0}?".format(self.filename),
                   QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.Yes):
            try:
                self.save()
            except EnvironmentError as e:
                QMessageBox.warning(self,
                        "G.R.O.M. Editor -- Save Error",
                        "Failed to save {0}: {1}".format(self.filename, e))


    def CursorPosition(self):
        line = self.textCursor().blockNumber()
        col = self.textCursor().columnNumber()




    def isModified(self):
        #self.emit(SIGNAL('MytextChanged(bool)'))
        return self.document().isModified()


    def save(self):
        if "Unnamed" in self.filename:
            filename = QFileDialog.getSaveFileName(self,
                    "G.R.O.M. Editor -- Save File As", self.filename,
                    "MD files (*.mdp *.itp *.top *.*)")
            print('filename is ',filename)
            if len(filename[0]) == 0:
                return
            self.filename = filename[0]
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.toPlainText()
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


    def load(self):
        exception = None
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.setPlainText(stream.readAll())
            self.document().setModified(False)
        except EnvironmentError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


# -*- coding: utf-8 -*-
"""
    GROM.textedit
    ~~~~~~~~~~~~~

    This is the main program with its GUI

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

from __future__ import absolute_import

from PyQt5.QtCore import (Qt,QFile, QFileInfo, QIODevice, QTextStream)
from PyQt5.QtGui import (QFont,QPainter, QColor,QTextCharFormat, QTextFormat)
from PyQt5.QtWidgets import (QTextEdit,QPlainTextEdit,QFileDialog, QWidget)

try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str

from  .GROMHighlight import GROMHighlighter
from  .frTextEdit import frTextObject


class LineNumberArea(QWidget):

    def __init__(self,editor):
        self.codeEditor=editor
        QWidget.__init__(self, editor)

    def sizeHint(self):
        return QtCore.QSize(self.codeEditor.lineNumberAreaWidth(),0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class TextEdit(QPlainTextEdit):

    NextId = 1

    FONT_MAX_SIZE = 30
    FONT_MIN_SIZE = 10

    def __init__(self, filename= None, parent=None):
        """
        Creates an Instance of QPlainTextEdit

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
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setWindowTitle(QFileInfo(self.filename).fileName())
        font = QFont("Courier", 11)
        self.document().setDefaultFont(font)
        self.setFont(font)
        self.setAutoFillBackground(False)
        self.setStyleSheet("QPlainTextEdit { background-color: rgb(30, 30, 30); color: rgb(154, 190, 154);}")

        #: Creates Syntax Highlighter and Find Replace Object for current Widget
        self.highlighter = GROMHighlighter(self.document())
        self.frTextObject = frTextObject(self)

        self.extraSelections = [[],[]] # [0] for selected Line, [1] for Search Results



        #: ---> Signals Start
        self.textChanged.connect(self.updateSearchText)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)

        self.updateRequest.connect(self.updateLineNumberArea)

        self.cursorPositionChanged.connect(self.highlightCurrentLine) #Need to fix this part
        #self.cursorPositionChanged.connect(self.CursorPosition)
        ##: ---> Signals End


        self.lineNumberArea = LineNumberArea(self)
        self.updateLineNumberAreaWidth(0)
        self.errorPos=None
        self.highlightCurrentLine() #Need to fix this part


    def lineNumberAreaPaintEvent(self, event): #When text zoomed line number not zoomed
        painter=QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber();
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():



            if block.isVisible() and bottom >= event.rect().top():
                font_original = self.document().defaultFont()
                size = font_original.pointSize()
                font = painter.font()
                font.setPointSize(size)
                painter.setFont(font)

                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(),
                    self.fontMetrics().height(),
                    Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber+=1

    def lineNumberAreaWidth(self):
        digits = 1
        _max = max (1, self.blockCount())
        while (_max >= 10):
            _max = _max/10
            digits+=1
        space = 5 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy);
        else:
            self.lineNumberArea.update(0, rect.y(),
                self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, e):
        QPlainTextEdit.resizeEvent(self,e)
        self.cr = self.contentsRect()
        self.lineNumberArea.setGeometry(self.cr.left(),
                                        self.cr.top(),
                                        self.lineNumberAreaWidth(),
                                        self.cr.height())

    def highlightError(self,pos):
        self.errorPos=pos
        self.highlightCurrentLine()


    def highlightCurrentLine(self):
        self.extraSelections[0] = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection() #
            lineColor = QColor(38,38,38)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            self.extraSelections[0].append(selection)

            if self.errorPos is not None:
                errorSel = QPlainTextEdit.ExtraSelection()
                lineColor = QColor(Qt.red).lighter(160)
                errorSel.format.setBackground(lineColor)
                errorSel.format.setProperty(QTextFormat.FullWidthSelection, True)
                errorSel.cursor = QTextCursor(self.document())
                errorSel.cursor.setPosition(self.errorPos)
                errorSel.cursor.clearSelection()
                self.extraSelections[0].append(errorSel)


        extra = self.extraSelections[0] + self.extraSelections[1]
        self.setExtraSelections(extra)


    def checkChange(self):
        print('blah blah time to see')

    def zoom_in(self):
        font = self.document().defaultFont()
        size = font.pointSize()
        if size < self.FONT_MAX_SIZE:
            size += 2
            font.setPointSize(size)
        self.setFont(font)
        #print('tada ',self.fontMetrics().height())


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
        self.frTextObject.replaceAll(findText,replaceAllText)


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


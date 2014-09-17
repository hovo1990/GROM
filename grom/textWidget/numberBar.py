# -*- coding: utf-8 -*-

#The MIT License
#Copyright (c) 2009 John Schember

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the “Software”), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE

#from PyQt4.Qt import QFrame
#from PyQt4.Qt import QWidget
#from PyQt4.Qt import QTextEdit
#from PyQt4.Qt import QHBoxLayout
#from PyQt4.Qt import QPainter
#from PyQt4.Qt import QApplication

from PyQt5.QtCore import (Qt,QFile, QFileInfo, QIODevice, QTextStream)
from PyQt5.QtGui import (QFont,QPainter, QColor,QTextCharFormat, QTextFormat)
from PyQt5.QtWidgets import (QFrame,QTextEdit,QFileDialog, QWidget,QApplication)



import sys

class NumberBar(QWidget):

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args)
        self.setTextEdit(kwargs.pop('edit', None))
        # This is used to update the width of the control.
        # It is the highest possible line number.
        self.highest_line = 1

    def setTextEdit(self, edit):
        if edit is None:
            return
        self.edit = edit
        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)

    def update(self, *args):
        '''
        Updates the number bar to display the current set of numbers.
        Also, adjusts the width of the number bar if necessary.
        '''
        # The + 4 is used to compensate for the current line being bold.
        width = self.fontMetrics().width(str(self.highest_line)) + 4
        if self.width() != width:
            self.setFixedWidth(width)
        QWidget.update(self, *args)

    def paintEvent(self, event):
        contents_y = self.edit.verticalScrollBar().value()
        page_bottom = contents_y + self.edit.viewport().height()
        font_metrics = self.fontMetrics()
        current_block = self.edit.document().findBlock(self.edit.textCursor().position())

        painter = QPainter(self)

        line_count = 0
        # Iterate over all text blocks in the document.
        block = self.edit.document().begin()
        while block.isValid():
            line_count += 1

            # The top left position of the block in the document
            position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

            # Check if the position of the block is out side of the visible
            # area.
            if position.y() > page_bottom:
                break

            # We want the line number for the selected line to be bold.
            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).
            painter.drawText(self.width() - font_metrics.width(str(line_count)) - 3,
                round(position.y()) - contents_y + font_metrics.ascent()+3,
                str(line_count))

            # Remove the bold style if it was set previously.
            if bold:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)

            block = block.next()

        self.highest_line = line_count
        painter.end()

        QWidget.paintEvent(self, event)

    def eventFilter(self, object, event):
        # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.
        if object in (self.edit, self.edit.viewport()):
            self.update()
            return False
        return QFrame.eventFilter(object, event)



    def getTextEdit(self):
        return self.edit

#def main(args=sys.argv):
    #app = QApplication(args)

    #editor = QTextEdit()
    #nb=NumberBar(edit=editor)
    #nb.show()
    #editor.show()

    #return app.exec_()

#if __name__ == '__main__':
    #sys.exit(main())

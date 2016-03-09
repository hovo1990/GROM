# -*- coding: utf-8 -*-
from PyQt5.QtCore import  Qt
from PyQt5.QtCore import QFileInfo

#: Importing from  PyQt5.QtWidgets

from PyQt5.QtWidgets import QWidget


from ColorTables import *

from Session import *
from TerminalDisplay import *
from KeyboardTranslator import *
from ColorScheme import *


class TermWidgetImpl(QWidget):

    def __init__(self):
        super(TermWidgetImpl, self).__init__()
        m_terminalDisplay = TerminalDisplay()
        m_session = Session()

        m_session.createSession()
        m_terminalDisplay.createTerminalDisplay(m_session, self)





class QTermWidget(QWidget):

    NoScrollBar=0
    ScrollBarLeft=1
    ScrollBarRight=2
    scrollBarPosition = []

    def __init__(self):
        super(QTermWidget, self).__init__()


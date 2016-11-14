# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PyQt4.QtGui import QApplication
# import atexit
from pyqterm import *

# Very slow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TerminalWidget()
    win.resize(800, 600)
    win.show()
    app.exec_()

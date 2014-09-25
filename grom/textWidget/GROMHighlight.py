# -*- coding: utf-8 -*-
"""
    GROM.GROMHighlight
    ~~~~~~~~~~~~~

    Module provides Syntax Highlighting for .mdp, .itp, .top files that used
    by G.R.O.M.A.C.S.

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""



import sys
import re

#: Import from PyQt5.QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegularExpression

#: Import from PyQt5.QtQtGui
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5.QtGui import QTextCharFormat





from .keyWords import Total
sys.path.append('ui/')

class GROMHighlighter(QSyntaxHighlighter):

    Rules = []
    Red_Rules = []
    Algorithm_Rules = []

    #: Regex pattern to find words
    WORDS = r"(?iu)[\w\-']+"

    def __init__(self, parent=None):
        super(GROMHighlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.blue)
        keywordFormat.setFontWeight(QFont.Bold)
        self.keyFormatAdress = keywordFormat


        #: adds all dictionary content to Rules
        for section in Total:
            keys = list(section.keys())
            for i in keys:
                list_is = section[i]
                GROMHighlighter.Red_Rules.append(i[2:-2])
                if len(list_is) > 0:
                    for element in list_is:
                        text = r"\b%s\b" %(element[2:-2])
                        GROMHighlighter.Red_Rules.append(text)
                        GROMHighlighter.Algorithm_Rules.append(text)
                        GROMHighlighter.Rules.append((QRegularExpression(text,QRegularExpression.CaseInsensitiveOption), keywordFormat)) #testing for underline yellow


        topolFormat = QTextCharFormat()
        topolFormat.setForeground(Qt.yellow)
        topolFormat.setFontWeight(QFont.Bold)
        for pattern_top in ((r"\[ defaults \]", r"\[ moleculetype \]", r"\[ atoms \]",r"\[ atomtypes \]",
                r"\[ bonds \]", r"\[ pairs \]", r"\[ angles \]",
                r"\[ dihedrals \]", r"\[ system \]", r"\[ molecules \]",r"\[ position_restraints \]")):
            GROMHighlighter.Rules.append((QRegularExpression(pattern_top),
                                           topolFormat))


        #--> Rule for 'N' to color red
        NoFormat = QTextCharFormat()
        NoFormat.setForeground(Qt.red)
        NoFormat.setFontWeight(QFont.Bold)
        pattern_No = r"\bN\b"
        GROMHighlighter.Rules.append((QRegularExpression(pattern_No),
                                           NoFormat))

        #--> Rule for 'Y' to color green
        YesFormat = QTextCharFormat()
        YesFormat.setForeground(Qt.green)
        YesFormat.setFontWeight(QFont.Bold)
        pattern_Yes = r"\bY\b"
        GROMHighlighter.Rules.append((QRegularExpression(pattern_Yes),
                                           YesFormat))



        #--> Rules for number patterns  to color orange
        number = QTextCharFormat()
        number.setForeground(QColor(255, 165, 0))
        number.setFontWeight(QFont.Bold)
        patternNum1 = QRegularExpression(r'\s[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?')
        patternNum2 = QRegularExpression(r'\s[+-]?[0-9]+[lL]?\s",r"\s[+-]?[0-9]+[lL]?\n')
        patternNum3 = QRegularExpression(r"\s[+-]?0[xX][0-9A-Fa-f]+[lL]?\s")
        patternNum4 = QRegularExpression(r"\s[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\s")
        GROMHighlighter.Rules.append((patternNum1, number))
        GROMHighlighter.Rules.append((patternNum2, number))
        GROMHighlighter.Rules.append((patternNum3, number))
        GROMHighlighter.Rules.append((patternNum4, number))


        #: --> Rule to color #include to darkCyan
        keywordInclude = QTextCharFormat()
        keywordInclude.setForeground(Qt.darkCyan)
        keywordInclude.setFontWeight(QFont.Bold)
        patternkeyGroIncl = QRegularExpression(  r"(#include).*$")
        GROMHighlighter.Rules.append((patternkeyGroIncl, keywordInclude))

        #: --> Rule to color #ifdef and #endif
        keywordIf = QTextCharFormat() #Here My Modif
        keywordIf.setForeground(QColor(180,202,138,220))
        keywordIf.setFontWeight(QFont.Bold)
        patternkeyGroIf = QRegularExpression(
                                  r"(#ifdef).*$"
                                  r"|(#endif).*$")
        GROMHighlighter.Rules.append((patternkeyGroIf, keywordIf))

        #: --> Rule to color POSRE
        POSREformat = QTextCharFormat()
        POSREformat.setForeground(QColor(255,85,0))
        POSREformat.setFontWeight(QFont.Bold)
        patternPOSRE = QRegularExpression(r"(-DPOSRE).*$")
        GROMHighlighter.Rules.append((patternPOSRE , POSREformat))


        #: --> Rule to color title to yellow
        titleFormat = QTextCharFormat()
        titleFormat.setForeground(QColor(3, 168, 250))
        titleFormat.setFontItalic(True)
        titleFormat.setFontWeight(QFont.Bold)
        GROMHighlighter.Rules.append((QRegularExpression(r"title[^\n]*"),
                                        titleFormat))


        #: --> Rule for Gromacs comment to color green
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(0, 127, 0))
        commentFormat.setFontItalic(True)
        commentFormat.setFontWeight(QFont.Bold)
        GROMHighlighter.Rules.append((QRegularExpression(r";[^\n]*"),
                                        commentFormat))



    def spellCheck(self,text,Rule1,Rule2):
        """
        Method defines to underline text if word not in Rules

        Args:
             text (str):  current text block to search
             Rule1 (list): GROMHighlighter.Red_Rules contains all words
             Rule2 (list ) GROMHighlighter.Algorithm_Rules only Algorithm rules
        """

        #: Underline words color yellow
        format_under = QTextCharFormat()
        format_under.setUnderlineColor(Qt.yellow)
        format_under.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

        #: Underlines word if not in Rules
        for word_object in re.finditer(self.WORDS, text,re.IGNORECASE):
            comment_location = text.find(';')
            word = word_object.group()
            if (word not in  Rule1  or word in  Rule2 or text[:comment_location].count(str(word)) > 1):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(),   format_under)

    def highlightBlock(self, text):
        """
        Method defines syntax highlighting and underlining

        Args:
             text (str):  current text block to search
        """

        self.spellCheck(text, GROMHighlighter.Red_Rules,
                        GROMHighlighter.Algorithm_Rules)

        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE = range(3)



        #Used to highlight according to its Rules
        for regex, format in GROMHighlighter.Rules: #Works This is a better Choice
            startpos = 0
            match = regex.globalMatch(text, startpos)
            while match.hasNext():
                i  = match.next()
                iCont = i.capturedTexts()[0]
                comment_location = text.find(';')
                number_of_times = text[:comment_location].count(iCont)
                if number_of_times > 1 and format == self.keyFormatAdress:
                    pass
                else:
                    for index in range(i.lastCapturedIndex() + 1):
                            self.setFormat(i.capturedStart(index), i.capturedLength(index), format)




        self.setCurrentBlockState(NORMAL)
        #if self.stringRe.indexIn(text) != -1:
            #return
# -*- coding: utf-8 -*-
"""
    GROM.pdb_model_0_88
    ~~~~~~~~~~~~~

    This is a custom model for  working with PDB files for QTableView  widget

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

import platform
import re
from PyQt5.QtCore import  (QModelIndex,QAbstractTableModel,
                           QSize, Qt, pyqtSignal)
from PyQt5.QtGui import (QColor, QTextDocument)
from PyQt5.QtWidgets import (QWidget, QStyledItemDelegate, QUndoStack,
                             QUndoCommand, QComboBox,QSpinBox,QDoubleSpinBox,
                             QLineEdit)
#import richtextlineedit


from .undoCommands import CommandElementChange
import tableWidget.PDB_parse as PDB_parse


comitDataSignal = pyqtSignal(QWidget , name = "commitData" )
closeEditorSignal = pyqtSignal(QWidget, name = "closeEditor")



try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str

(ATOM, serial, name, resName,
 ChainID, resNum,X,Y,Z, occupancy, charge, element) = range(12)



MAGIC_NUMBER = 0x570C4
FILE_VERSION = 1



class PDB_rowInfo(object):


    def __init__(self, ATOM,ATOM_TextColor, serial, name, resName,ChainID,
                ChainID_color,  resNum,resNum_color, X,Y,Z, occupancy,
                charge, element):
        """
        Method defines a single row of a PDB file

        Args:
             ATOM (str):  values are [ATOM, HETATM]
             ATOM_TextColor (QColor): blue for 'ATOM' and red for 'HETATM'
             serial (int) Atom  serial number
             name (str) Atom Name
             resName (str) Residue Name
             ChainID (str) Chain identifier
             ChainID_color (QColor) ChainID Color
             resNum (int)  Residue sequence number.
             resNum_color (QColor) diffent color for resNum
             X (float) Orthogonal coordinates for X in Angstroms.
             Y (float) Orthogonal coordinates for Y in Angstroms.
             Z (float) Orthogonal coordinates for Z in Angstroms.
             occupancy (float) Occupancy
             charge (float) Charge of the ATOM
             element (str) Atom Name
        """
        self.ATOM = ATOM
        self.ATOM_TextColor = ATOM_TextColor
        self.serial  = serial
        self.name = name
        self.resName = resName
        self.ChainID = ChainID
        self.ChainID_initial  = ChainID
        self.ChainID_color = ChainID_color
        self.ChainID_color_initial = ChainID_color
        self.resNum  = resNum
        self.resNum_initial  = resNum
        self.resNum_color = resNum_color
        self.resNum_color_initial = resNum_color
        self.X = X
        self.Y = Y
        self.Z = Z
        self.occupancy = occupancy
        self.charge = charge
        self.element = element
        self.access = {0:self.ATOM, 1:self.serial, 2:self.name, 3:self.resName,
                       4:self.ChainID, 5:self.resNum, 6:self.X, 7:self.Y,
                       8:self.Z, 9:self.occupancy, 10:self.charge,
                       11:self.element}

    def __hash__(self):
        return super(PDB_rowInfo, self).__hash__()


    def __lt__(self, other):
        return self.name.lower() < other.name.lower()


    def __eq__(self, other):
        return self.name.lower() == other.name.lower()


class PDB_Container(object):

    def __init__(self, filename=""):
        self.filename = filename
        self.dirty = False
        self.PDB_ROWS = {}


    def PDB(self, identity):
        return self.PDB_ROWS.get(identity)



    def __len__(self):
        return len(self.PDB_ROWS)


    def __iter__(self):
        for PDB_ROW in self.PDB_ROWS.values():
            yield PDB_ROW


    def inOrder(self):
        return sorted(self.PDB_ROWS.values())


    def load(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            self.mol,info_ready = PDB_parse.PDBparse(self.filename)
            for row in self.mol:
                ATOM = row[0]
                serial = row[1]
                name = row[2]
                resName = row[3]
                ChainID = row[4]
                resNum = row[5]
                X = row[6]
                Y = row[7]
                Z = row[8]
                occupancy = row[9]
                charge = row[10]
                element = row[11]
                PDBrow = PDB_rowInfo(ATOM, serial, name, resName,ChainID, resNum,X,Y,Z, occupancy, charge, element)
                self.PDB_ROWS[id(PDBrow)] = PDBrow
            self.dirty = False
        except IOError as e:
            exception = e



    def save(self):
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for saving")
        except IOError as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            if exception is not None:
                raise exception


class PDBTableModel(QAbstractTableModel): #This part is the ultimate important part



    def __init__(self, filename=""):
        """
        Method defines a custom Model for working with PDB for Table Widget

        Args:
             filename (str) filename if opened
        """
        super(PDBTableModel, self).__init__()
        self.filename = filename
        self.dirty = False
        self.PDB_rows = []
        self.resNum_temp = 1


    def sortByName(self):
        self.PDB_rows = sorted(self.PDB_rows)
        self.reset()


    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(
                QAbstractTableModel.flags(self, index)|
                Qt.ItemIsEditable)


    def data(self, index, role=Qt.DisplayRole):
        PDB_row = self.PDB_rows[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == ATOM:
                return PDB_row.ATOM
            elif column == serial: ####################Continue from Here (ATOM, serial, name, resName, ChainID, resNum,X,Y,Z, occupancy, charge, element) = range(12)
                return PDB_row.serial
            elif column == name:
                return PDB_row.name
            elif column == resName:
                return PDB_row.resName
            elif column == ChainID:
                return PDB_row.ChainID
            elif column == resNum:
                return PDB_row.resNum
            elif column == X:
                return PDB_row.X
            elif column == Y:
                return PDB_row.Y
            elif column == Z:
                return PDB_row.Z
            elif column ==  occupancy:
                return PDB_row.occupancy
            elif column == charge:
                return PDB_row.charge
            elif column == element:
                return PDB_row.element
        elif role == Qt.BackgroundRole:
            if column == resNum:
                return  PDB_row.resNum_color
            elif column == ChainID:
                return PDB_row.ChainID_color
        elif role == Qt.TextColorRole:
            if column == ATOM:
                return PDB_row.ATOM_TextColor
            elif column == X:
                return QColor(Qt.red)
            elif column == Y:
                return QColor(Qt.green)
            elif column == Z:
                return QColor(Qt.blue)
            elif column == charge:
                return QColor(Qt.darkYellow)
        return None


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft|Qt.AlignVCenter)
            return int(Qt.AlignRight|Qt.AlignVCenter)
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == ATOM:
                return 'ATOM'
            elif section == serial: ####################Continue from Here (ATOM, serial, name, resName, ChainID, resNum,X,Y,Z, occupancy, charge, element) = range(12)
                return 'serial'
            elif section == name:
                return 'name'
            elif section == resName:
                return 'resName'
            elif section == ChainID:
                return 'ChainID'
            elif section == resNum:
                return 'resNum'
            elif section == X:
                return 'X'
            elif section == Y:
                return 'Y'
            elif section == Z:
                return 'Z'
            elif section ==  occupancy:
                return 'occupancy'
            elif section == charge:
                return 'charge'
            elif section == element:
                return 'element'
        return int(section + 1)



    def rowCount(self, index=QModelIndex()):
        return len(self.PDB_rows)


    def columnCount(self, index=QModelIndex()):
        return 12


    def setData(self, index, value, role=Qt.EditRole):
        """
        Method defines for setting up Data

        Args:
             index (QIndex*) index of the model
             value (str) modifies value at current selected index
        """
        if index.isValid() and 0 <= index.row() < len(self.PDB_rows):
            PDB_row = self.PDB_rows[index.row()]
            column = index.column()
            if column == ATOM:
                PDB_row.ATOM = value
                if PDB_row.ATOM == 'ATOM':
                    PDB_row.ATOM_TextColor = QColor(Qt.darkBlue)
                else:
                    PDB_row.ATOM_TextColor = QColor(144,0,0)
            elif column == serial:
                 PDB_row.serial = value
            elif column == name:
                 PDB_row.name = value
            elif column == resName:
                PDB_row.resName = value
            elif column == ChainID:
                 PDB_row.ChainID = value
                 if PDB_row.ChainID_initial != PDB_row.ChainID:
                     PDB_row.ChainID_color = QColor(138,43,226)
                 else:
                     PDB_row.ChainID_color = PDB_row.ChainID_color_initial
            elif column == resNum:
                 PDB_row.resNum = int(value)
                 if int(PDB_row.resNum_initial) != int(PDB_row.resNum):
                     PDB_row.resNum_color = QColor(255,165,0)
                 else:
                     PDB_row.resNum_color = PDB_row.resNum_color_initial
            elif column == X:
                 PDB_row.X = float(value)
            elif column == Y:
                 PDB_row.Y = float(value)
            elif column == Z:
                 PDB_row.Z = float(value)
            elif column ==  occupancy:
                 PDB_row.occupancy = value
            elif column == charge:
                PDB_row.charge = value
            elif column == element:
                PDB_row.element = value
            self.dirty = True
            self.dataChanged.emit(index,index)
            return True
        return False


    def getRow(self,position):
        return self.PDB_rows[position]


    def customInsertRows(self, position, row_data,rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.PDB_rows.insert(position + row,row_data)
        self.endInsertRows()
        self.dirty = True
        return True

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.PDB_rows.insert(position + row,
                              PDB_rowInfo("Unknown", "Unknown"," Unknown",
                                          "Unknown"," Unknown", " Unknown",
                                          "Unknown"," Unknown", " Unknown",
                                          " Unknown"," Unknown", " Unknown",
                                          " Unknown"," Unknown", " Unknown"))
        self.endInsertRows()
        self.dirty = True
        return True


    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.PDB_rows = (self.PDB_rows[:position] +
                      self.PDB_rows[position + rows:])
        self.endRemoveRows()
        self.dirty = True
        return True



    def load(self,fname): #This parts need modification
        self.filename = fname
        exception = None
        fh = None
        try:
            if self.filename != '':
                if not self.filename:
                    raise IOError("no filename specified for loading")
                self.PDB_rows = []
                self.mol,info_ready = PDB_parse.PDBparse(self.filename)
                #print('self.mol is ',self.mol)
                self.flag_color = True
                self.val = 1
                self.chainFlag = True
                self.ChainID_tempVal_color = self.mol[0][4]
                for row in self.mol:
                    ATOM = row[0]
                    if ATOM == 'ATOM':
                        ATOM_TextColor = QColor(Qt.darkBlue)
                    else:
                        ATOM_TextColor = QColor(144,0,0)
                    serial = row[1]
                    name = row[2]
                    resName = row[3]
                    ChainID = row[4]
                    resNum = row[5]
                    if self.ChainID_tempVal_color != ChainID :
                            if self.chainFlag == True:
                                self.chainFlag = False
                                #self.val = int(resNum)
                                ChainID_color = QColor(Qt.cyan)
                            elif self.chainFlag == False:
                                self.chainFlag = True
                                #self.val = int(PDB_row.resNum)
                                ChainID_color = QColor(Qt.lightGray)
                            self.ChainID_tempVal_color = ChainID
                    elif self.chainFlag  == True and self.ChainID_tempVal_color == ChainID:
                        ChainID_color = QColor(Qt.lightGray)
                    elif self.chainFlag  == False and self.ChainID_tempVal_color == ChainID:
                        ChainID_color = QColor(Qt.cyan)
                    if self.val != int(resNum):
                            if self.flag_color == True:
                                self.flag_color = False
                                #self.val = int(resNum)
                                resNum_color = QColor(Qt.green)
                            elif self.flag_color == False:
                                self.flag_color = True
                                #self.val = int(PDB_row.resNum)
                                resNum_color = QColor(Qt.yellow)
                            self.val = int(resNum)
                    elif self.flag_color == True and self.val == int(resNum):
                        resNum_color = QColor(Qt.yellow)
                    elif self.flag_color == False and self.val == int(resNum):
                        resNum_color = QColor(Qt.green)
                    X = row[6]
                    Y = row[7]
                    Z = row[8]
                    occupancy = row[9]
                    charge = row[10]
                    element = row[11]
                    PDBrow = PDB_rowInfo(ATOM, ATOM_TextColor,serial, name, resName,ChainID,ChainID_color, resNum,resNum_color, X,Y,Z, occupancy, charge, element)
                    #print('PDBrow is ',PDBrow.getValues())
                    self.PDB_rows.append(PDBrow)
                    self.dirty = False
        except IOError as e:
                exception = e
        finally:
                if fh is not None:
                    fh.close()
                if exception is not None:
                    raise exception



    def save(self,filename):
        self.filename = filename
        exception = None
        open_file = None
        try:
            if not self.filename:
                raise IOError("no filename specified for saving")
            open_file = open(self.filename,'w')
            for row in self.PDB_rows:
                atom = row.ATOM
                serial = row.serial
                name = row.name
                resName = row.resName
                chainID  = row.ChainID
                resNum = row.resNum
                x = row.X
                y = row.Y
                z = row.Z
                occupancy = row.occupancy
                charge = row.charge
                element = row.element
                line= [atom,serial,name,resName,chainID,resNum,x,y,z,occupancy,charge,element]
                #print('line is ',line)
                PDB_parse.write_SingleLine_to_PDB(open_file,line)
            self.dirty = False
        except IOError as e:
            exception = e
        finally:
            if open_file is not None:
                open_file.close()
            if exception is not None:
                raise exception


class PDBDelegate(QStyledItemDelegate):


    def __init__(self, parent=None):
        super(PDBDelegate, self).__init__(parent)
        self.undoStack = QUndoStack(self) #This is for undo/redo




    def paint(self, painter, option, index):
            QStyledItemDelegate.paint(self, painter, option, index)


    def sizeHint(self, option, index):
        fm = option.fontMetrics
        if index.column() == ATOM:
            return QSize(fm.width("9,999,999"), fm.height())
        if index.column() == resName:
            text = index.model().data(index)
            document = QTextDocument()
            document.setDefaultFont(option.font)
            document.setHtml(text)
            return QSize(document.idealWidth() + 5, fm.height())
        return QStyledItemDelegate.sizeHint(self, option, index)


    def createEditor(self, parent, option, index):
        if index.column() == ATOM:
            combobox = QComboBox(parent)
            combobox.addItems(['ATOM','HETATM'])
            combobox.setEditable(True)
            return combobox
        elif index.column() == serial:
            spinbox = QSpinBox(parent)
            spinbox.setRange(1, 200000)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        elif index.column() == name:
            editor = QLineEdit(parent)
            editor.returnPressed.connect(self.commitAndCloseEditor)
            return editor
        elif index.column() == resName:
            editor = QLineEdit(parent)
            editor.returnPressed.connect(self.commitAndCloseEditor)
            return editor
        elif index.column() == ChainID:
            editor = QLineEdit(parent)
            editor.returnPressed.connect(self.commitAndCloseEditor)
            return editor
        elif index.column() == resNum:
            spinbox = QSpinBox(parent)
            spinbox.setRange(1, 200000)
            spinbox.setSingleStep(1)
            spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return spinbox
        elif index.column() in (X,Y,Z,occupancy,charge): ###this works
            dspinbox = QDoubleSpinBox(parent)
            dspinbox.setRange(-200000, 200000)
            dspinbox.setSingleStep(0.1)
            dspinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return dspinbox
        else:
            return QStyledItemDelegate.createEditor(self, parent, option,
                                                    index)




    def commitAndCloseEditor(self):
        editor = self.sender()
        if isinstance(editor, (QTextEdit, QLineEdit)):
            comitDataSignal.emit(editor)
            closeEditorSignal .emit(editor)




    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        if index.column() == name:
            editor.setText(text)
        elif index.column() == resName:
            editor.setText(text)
        elif  index.column() == ChainID:
            editor.setText(text)
        elif  index.column() == resNum:
            if text is None:
                value = 0
            elif isinstance(text, int):
                value = text
            else:
                value = int(re.sub(r"[., ]", "", text))
            editor.setValue(value)
        elif  index.column() in (serial,X,Y,Z,occupancy,charge):
            if text is None:
                value = 0
            elif isinstance(text, int):
                value = text
            else:
                value = float( text)
            editor.setValue(value)
        elif index.column() == element:
            editor.setText(text)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):
        command = CommandElementChange(self, editor, model, index,
                             "Change item value")
        self.undoStack.push(command)

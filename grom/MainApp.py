# -*- coding: utf-8 -*-
"""
    GROM.MainApp
    ~~~~~~~~~~~~~

    This is the main program with its GUI

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

from __future__ import absolute_import
import os
import sys
import platform
sys.path.append('grom/')

#: Importing from  PyQt5.QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFileInfo
from PyQt5.QtCore import QUrl


#: Importing from  PyQt5.QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QUndoStack
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMenu

#: Importing from  PyQt5.QtWebKitWidgets
from  PyQt5.QtWebKitWidgets import QWebPage

from  ui import ui_mainWindow as MW #Imports MainWindow GUI
from customQProcess import *

import findandreplacedlg #Search Dialog

import Icons_rc



from textWidget import textedit # Imports custom Text Editor

from tableWidget import  tableView  #Imports custom TableView widget

from plotWidget import plotTool #Imports Gromacs edr Plot Tool

from modules import *  #Import various modules for Help, MultiRename and Choose Dialog Widgets



#: PyQt for Python 3 doesn't use QString
try:
    from PyQt5.QtCore import QString
except ImportError:
     #we are using Python3 so QString is not defined
    QString = str



__version__ = "0.6.5.0"


#file_formats = "*.pdb *.gro *.mdp *.itp *.top"
file_formats = "*.pdb *.gro *.mdp *.itp *.top *.edr" #Adding new format .edr


folder_mainAPP = os.path.realpath(__file__)[:-15]
__current_directory__ = folder_mainAPP
#print('folder mainAPP ',folder_mainAPP)



class MainWindow(QMainWindow,MW.Ui_MainWindow):
    """
    This is the Main Window and the application
    Inherits QMainWindow and MW.Ui_MainWindow GUI functions and its methods

    """
    Instances = set()
    Search_Window = None
    Search_Dialog_activated = False

    index_tabs  = 0
    tabs_allowed = 25
    moreFrame_show = False


    def __init__(self,filename = None, parent = None):
        super(MainWindow, self).__init__(parent)

        #: sets Up GUI from  MW.Ui_MainWindow
        self.setupUi(self)
        self.version = __version__

        #: lists defines combobox content for Help
        lists = ['mdp options(v5.0)','mdp options(v4.6)','PDB file structure']
        self.comboBox.addItems(lists)
        self.keylist = [] #For detecting pressed keys




        #: Detect OS
        self.detectOS()
        self.setFocusPolicy(Qt.StrongFocus)

        #: disables help Widget
        self.moreFrame_open = False
        self.state = 'editor'
        self.filename = filename
        self.parent = parent

        self.setAttribute(Qt.WA_DeleteOnClose)
        MainWindow.Instances.add(self) #Look in this one



        self.qProcess = CustomQProcess() #VIT
        self.qProcess.finished.connect(self.delTempFile) #This is it !!!!


        self.undoStack = QUndoStack(self)
        self.setWindowTitle("G.R.O.M. Editor") #Sets application Title

        self.inactivateEssential() # Inactivates widgets


        self.tabWidget.setTabsClosable(True) #Set Tabs closable

        # --> Sets up all the necessary Signals
        self.actionIconNew.triggered.connect(self.chooseNew)
        self.actionIconOpen.triggered.connect(self.FileOpen)
        self.actionIconSave.triggered.connect(self.fileSave)
        self.actionIconSaveAs.triggered.connect(self.fileSaveAs)
        self.actionExit.triggered.connect(self.fileQuit)
        self.actionIconHelp.triggered.connect(self.showHelpMenu)
        self.actionCopy.triggered.connect(self.editCopy)
        self.actionPaste.triggered.connect(self.editPaste)

        self.actionCut.setShortcutContext(Qt.ApplicationShortcut)
        self.actionCut.triggered.connect(self.editCut)
        self.actionSelect_All.triggered.connect(self.editSelectAll)
        self.actionDeselect_All.triggered.connect(self.editDeselectAll)
        self.actionUndo.triggered.connect(self.editUndo)
        self.actionRedo.triggered.connect(self.editRedo)
        self.actionFind.triggered.connect(self.FindReplace)
        self.actionReplace.triggered.connect(self.FindReplace)
        self.actionZoom_In.triggered.connect(self.ZoomIn)
        self.actionZoom_Out.triggered.connect(self.ZoomOut)
        self.actionAbout_Qt.triggered.connect(self.showAboutQt)
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionMulti_Rename.triggered.connect(self.MultiRename)
        self.actionAdd_Row.triggered.connect(self.tableAdd_Row)
        self.actionRemove_Row.triggered.connect(self.tableRemove_Row)
        self.actionRenumerate.triggered.connect(self.ResNumFix)
        self.actionComment.triggered.connect(self.commentLine)
        self.actionUncomment.triggered.connect(self.uncommentLine)

        #: THis part is for viewing coordinate files in molecular editors
        self.actionOpen_in_VMD.triggered.connect(self.openVMD)
        self.actionOpen_in_PyMol.triggered.connect(self.openPyMol)
        self.actionOpen_in_Avogadro.triggered.connect(self.openAvogadro)


        self.tabWidget.blockSignals(False)

        self.tabWidget.currentChanged.connect(self.configureStuff)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.destroyed.connect(MainWindow.updateInstances)
        #----> SIGNALS END

        #: if tab count more than allowed show warning
        if self.tabWidget.count() >  self.tabs_allowed:
            QMessageBox.warning(self,"Oops",'No more tabs are allowed')


    def delTempFile(self):
        try:
            print("Yolo Hahahahahahahaha")
            os.remove(self.tempFileName)
            print("Print Temp File Deleted")
        except Exception as e:
            print("Error in deleting file: ",e)

    def openVMD(self):
        currentWidget = self.tabWidget.currentWidget()
        #currentFile = currentWidget.getFileName()
        self.tempFileName = currentWidget.saveTempFile()
        self.qProcess.startVMD(self.tempFileName,currentWidget)
        #self.qProcess.start("vmd %s" %self.tempFileName)


    def openPyMol(self):
        currentWidget = self.tabWidget.currentWidget()
        #currentFile = currentWidget.getFileName()
        self.tempFileName = currentWidget.saveTempFile()
        self.qProcess.startPYMOL(self.tempFileName,currentWidget)
        #self.qProcess.start("pymol %s" %self.tempFileName)

    def openAvogadro(self):
        currentWidget = self.tabWidget.currentWidget()
        #currentFile = currentWidget.getFileName()
        self.tempFileName = currentWidget.saveTempFile()
        self.qProcess.start("avogadro %s" %self.tempFileName)

    #def keyPressEvent(self,event):
        #if event.key()==(Qt.Key_Control and Qt.Key_F):
            #self.FindReplace()
        #elif event.key()==(Qt.Key_Control and Qt.Key_H):
            #self.FindReplace()
        #elif event.key()==(Qt.Key_Control and Qt.Key_N):
            #self.chooseNew()
        #elif event.key()==(Qt.Key_Control and Qt.Key_O):
            #self.FileOpen()
        #elif event.key()==(Qt.Key_Control and Qt.Key_S):
            #self.fileSave()
        ##else:
            #MainWindow.keyPressEvent(self,event)

    def commentLine(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.commentLine()
        except:
            pass


    def uncommentLine(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.uncommentLine()
        except:
            pass

    def keyPressEvent(self, event):
        self.firstrelease = True
        event_check = int(event.key())
        #event = event.key
        self.keylist.append(event_check)
        #print(self.keylist)
        Key_Control = 16777249
        Shift_Control = 16777248
        if event.key()==( Qt.Key_F1): #It should show if there action not activated
            self.showHelpMenu()
            return
        #try:
            #if Key_Control not in self.keylist:# or  Qt.Key_Shift not in self.keylist:
                ##print('Choice 1')
                #MainWindow.keyPressEvent(self,event)
                #return
        #except Exception as e:
            #print("Error in keyPressEvent ",e)
        #elif Shift_Control not in self.keylist:
            #print('Choice 2')
            #QPlainTextEdit.keyPressEvent(self,event)

    def keyReleaseEvent(self, event):
        try:
            if self.firstrelease == True:
                self.processmultikeys(self.keylist)


            self.firstrelease = False

            del self.keylist[-1]
        except:
            pass

    def processmultikeys(self,keyspressed):
        #print('keysPressed is ',keyspressed)
        if Qt.Key_Control  in keyspressed and Qt.Key_X in keyspressed:
            self.editCut()
        elif (Qt.Key_Control in keyspressed and Qt.Key_C in keyspressed):
            self.editCopy()
        elif (Qt.Key_Control in keyspressed and Qt.Key_V in keyspressed):
            self.editPaste()
        elif (Qt.Key_Control in keyspressed and Qt.Key_N in keyspressed):
            self.chooseNew()
        elif (Qt.Key_Control in keyspressed and Qt.Key_O in keyspressed):
            self.FileOpen()
        elif (Qt.Key_Control in keyspressed and Qt.Key_S in keyspressed):
            self.fileSave()
        #elif (Qt.Key_Control in keyspressed and Qt.Key_Shift in keyspressed and Qt.Key_D in keyspressed):
            #self.uncommentLine() #This is new
        #elif (Qt.Key_Control in keyspressed and Qt.Key_D in keyspressed):
            #self.commentLine() #this is new
        elif (Qt.Key_Control in keyspressed and Qt.Key_F in keyspressed):
            self.FindReplace()
        elif (Qt.Key_Control in keyspressed and Qt.Key_H in keyspressed):
            self.FindReplace()
        #elif (Qt.Key_Control in keyspressed and  Qt.Key_Plus in keyspressed):
            #self.ZoomIn()
        #elif (Qt.Key_Control in keyspressed and Qt.Key_Minus in keyspressed ):
            #self.ZoomOut()
        elif (Qt.Key_Control in keyspressed and Qt.Key_Shift in keyspressed and Qt.Key_A in keyspressed):
            self.editDeselectAll()
        elif (Qt.Key_Control in keyspressed and Qt.Key_A in keyspressed):
            self.editSelectAll()
        elif (Qt.Key_Control in keyspressed and Qt.Key_Shift in keyspressed and Qt.Key_Z in keyspressed):
            #print("redo Working")
            self.editRedo()
        elif (Qt.Key_Control in keyspressed and Qt.Key_Z in keyspressed):
            #print("undo working")
            self.editUndo()




    def closeTab(self,index):
        """
        This is the method to close a tab in TabWidget.
        if tabCount less than zero, deactivates Help and Actions.

         Args:
              index (int): index of the  closed Tab.

        """
        self.index_tabs -= 1
        self.tabWidget.removeTab(index)
        if self.index_tabs <=0:
            self.moreFrame_show = True
            self.showHelpMenu()
            self.inactivateEssential()




    @staticmethod
    def updateInstances( qobj): #check this out
        """
        THis method is used than not only MainWindow is active,but also Seach Dialog.
        if Search Dialog is open, and you close MainWindow, whole app is closed.

         Args:
              qobj (QObject*): reference of the Window Instacnce

        """
        MainWindow.Instances = (set([window for window
                in MainWindow.Instances if isAlive(window)]))
        for obj in list(MainWindow.Instances):
            if len(list(MainWindow.Instances)) <2:
                if obj.state == 'search':
                    sys.exit()
        MainWindow.Search_Dialog_activated = False

    def showAbout(self):
        """
        This method is for showing about GROM
        """
        text = "G.R.O.M is cross-platform  Parameter and Coordinate File Editor\n"
        text += "\n"
        text += "Version: %s\n" %(self.version)
        text += "Source Code: https://github.com/hovo1990/GROM"
        text += "\n"
        text += "Mail: hovakim_grabski@yahoo.com"
        text += "\n"
        text += "Author: Hovakim Grabski"
        QMessageBox.about(self,"About G.R.O.M.",text)

    def showAboutQt(self):
        QMessageBox.aboutQt(self,"About Qt")

    def ZoomIn(self):
        """
        Zoom In  for Text Editor.

        Keyword arguments:
        None
        """
        textEdit = self.tabWidget.currentWidget() #Gets the address of the current Widget in Tabs
        textEdit.zoom_in() #This fixes the problem

    def ZoomOut(self):
        """
        Zoom out for Text Editor.

        Keyword arguments:
        None
        """
        textEdit = self.tabWidget.currentWidget() #Gets the address of the current Widget in Tabs
        textEdit.zoom_out() #This fixes the problem with font


    def configureStuff(self):
        """
        This method is used than tab is changed.

        When tab is changed  Actions are changed corresponding if widget is
        text editor or table editor and updates Search Objects widget reference.
        """
        currentWidget = self.tabWidget.currentWidget()
        try:
            self.activateEssential(currentWidget)
            try:
                self.searchToMake()
            except:
                pass
        except Exception as error:
            self.showError(error)



    def fileQuit(self):
        #This closes application
        QApplication.closeAllWindows()


    def okToContinue(self):
        if self.textEdit.document().isModified():
            reply = QMessageBox.question(self,
                            "G.R.O.M. Editor - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True






    def getFileName(self,filename):
        temp = ''
        for i in filename[::-1]:
            if i != '/':
                temp += i
            elif i == '/':
                break
        return temp[::-1]



    def chooseNew(self):
        """
        This for choosing new file. Parameter or Coordinate File.
        """
        dialogOption = ChooseDialog()
        if dialogOption.exec_():
            if dialogOption.ParamButton.isChecked():
                    self.fileNewParam() #Need to work this out
            elif dialogOption.CoordButton.isChecked():
                if dialogOption.pdbButton.isChecked():
                    modelType = 'PDB'
                elif dialogOption.groButton.isChecked():
                    modelType = 'GRO'
                self.fileNewCoord(modelType)
            self.filename = "Untitled"
        #else:
            #QMessageBox.warning(self,'App','Dialog Canceled')





    def fileNewParam(self):
        #: This creates new Parameter File(.mdp,.itp,.top)
        #if not self.okToContinue():
            #return
        if self.tabWidget.count() < self.tabs_allowed  :
            self.showParamStuff()
        else:
            QMessageBox.warning(self,"Oops",'No more tabs are allowed')




    def fileNewCoord(self,modelType):
        #This creates new Coordinate File(.pdb)
        if self.tabWidget.count() < self.tabs_allowed  :
            self.showCoordStuff(modelType)
        else:
            print('Ouch')
            QMessageBox.warning(self,"Oops",'No more tabs are allowed')


    def loadEdrFile(self,filename):
        """
        Method for loading a Gromacs edr File
        """
        plotShow = plotTool.plotWidget(filename,self)
        #textEdit.customDataChanged.connect(self.changeTabName)
        #self.activateEssential(textEdit) #Activates QActions and Widgets
        self.tabWidget.show()
        try:
            #textEdit.load()
            #textEdit.frTextObject.getText()
            self.index_tabs += 1
        except EnvironmentError as e:
            QMessageBox.warning(self,
                    "G.R.O.M. Editor -- Load Error",
                    "Failed to load {0}: {1}".format(filename, e))
            plotShow.close()
            del plotShow
        else:
            self.tabWidget.addTab(plotShow, plotShow.windowTitle())
            self.tabWidget.setCurrentWidget(plotShow)




    def FileOpen(self):
        """This is for loading file and putting into QTable QTextEditor"""
        #if not self.okToContinue():
            #return
        directory = (os.path.dirname(self.filename)
                if self.filename is not None else __current_directory__)
        fname_load = QFileDialog.getOpenFileName(self,
                "G.R.O.M. Editor - Choose File", directory,
                "MD files ( %s )" %file_formats) #This import especially for edr Files
        fname = fname_load[0]
        print('fname is ',fname)
        #print("test case ",('pdb'  not in fname) or ('gro'  not in fname))
        if ('edr'  in fname):
            print("Oops edr File")
            self.loadEdrFile(fname)
        elif ('gro'  not in fname and 'pdb' not in fname): #Later need to add gro support Bug Here
                if not len(fname) < 2:
                    for i in range(self.tabWidget.count()):
                        textEdit = self.tabWidget.widget(i)
                        if textEdit.filename == fname:
                            self.tabWidget.setCurrentWidget(textEdit)
                            break
                    else:
                        self.loadParamFile(fname)
        else:
            try:
                self.loadCoordFile(fname)
            except Exception as e:
                print("Error in loading ",e)
                QMessageBox.warning(self,
                "G.R.O.M. Editor -- Load Error",
                "Please check your PDB/GRO file")

    def loadCoordFile(self, filename):
        """
        Method for loading a Coordinate File
        """
        tableWidget = tableView.TableEdit(filename,parent = self)
        tableWidget.customDataChanged.connect(self.changeTabName)
        self.activateEssential(tableWidget) #Activates QActions and Widgets
        self.customMenuCoord(tableWidget) #sets up custom Context Menu
        self.tabWidget.show()
        try:
            tableWidget.initialLoad() #Loads file
            self.index_tabs += 1
        except EnvironmentError as e:
            QMessageBox.warning(self,
                    "G.R.O.M. Editor -- Load Error",
                    "Failed to load {0}: {1}".format(filename,e))
            tableWidget.close()
            del tableWidget
        else:
            self.tabWidget.addTab(tableWidget, tableWidget.windowTitle())
            self.tabWidget.setCurrentWidget(tableWidget)


    def changeTabName(self):
        currentWidget = self.tabWidget.currentWidget()
        tempName = currentWidget.tempName
        self.tabWidget.setTabText(self.tabWidget.currentIndex(),tempName)


    def showError(self,error):
        """Opens a QMessageBox with the error message"""
        QMessageBox.warning(self,"Oops",'%s' %(error))

    def fileSave(self):
        """
        Method for saving currentWidget's content to File.
        If currentWidget is instance of TextEditor, save to parameter file.
        Else to coordinate File.
        """
        try:
            currentWidget = self.tabWidget.currentWidget()
            if  isinstance(currentWidget, QPlainTextEdit):
                try:
                    currentWidget.save()
                    self.tabWidget.setTabText(self.tabWidget.currentIndex(),
                            QFileInfo(currentWidget.filename).fileName())
                    print('save name ',currentWidget.filename)
                    #self.statusbar.showMessage('Finished Location: %s' %str(currentWidget.filename))
                    return True
                except EnvironmentError as e:
                    QMessageBox.warning(self,
                            "Tabbed Text Editor -- Save Error",
                            "Failed to save {0}: {1}".format(currentWidget.filename, e))
                    return False
            else:
                try:
                    currentWidget.save()
                    self.tabWidget.setTabText(self.tabWidget.currentIndex(),
                            QFileInfo(currentWidget.filename).fileName())
                    #self.statusbar.showMessage('Finished Location: %s' %str(currentWidget.filename))
                except Exception as e:
                    QMessageBox.warning(self,
                            "Tabbed Text Editor -- Save Error",
                            "Failed to save {0}: {1}".format(currentWidget.filename, e))
                    return False
        except Exception as e:
            #self.showError(e)
            print("Error is Save FIle ",e)
            pass


    def fileSaveAs(self): #Half has been achieved
        """
        Method for saving currentWidget's content to File.
        If currentWidget is instance of TextEditor, save to parameter file.
        Else to coordinate File.
        """
        try:
            currentWidget = self.tabWidget.currentWidget()
            if  isinstance(currentWidget, QPlainTextEdit):
                try:
                    filename = QFileDialog.getSaveFileName(self,
                        "G.R.O.M. Editor -- Save File As", currentWidget.filename,
                        "MD files (*.mdp *.itp *.top *.*)")
                    if len(filename[0]) == 0:
                        return
                    currentWidget.filename = filename[0]
                    self.statusbar.showMessage('Finished Location: %s' %str(currentWidget.filename))
                    return self.fileSave()
                except EnvironmentError as e:
                    QMessageBox.warning(self,
                            "Tabbed Text Editor -- Save Error",
                            "Failed to save {0}: {1}".format(currentWidget.filename, e))
                    return False
            else:
                try:
                    currentWidget.saveAs() #Need to modify for Tableview save asnte
                    self.tabWidget.setTabText(self.tabWidget.currentIndex(),currentWidget.windowTitle())
                    self.statusbar.showMessage('Finished Location: %s' %str(self.filename))
                    return True
                except Exception as e:
                    QMessageBox.warning(self,
                            "Tabbed Text Editor -- Save Error",
                            "Failed to save {0}: {1}".format(currentWidget.filename, e))
                    return False
        except Exception as error:
            print("Error in Save FIle As ",e)
            pass
           # self.showError(error)





    def loadParamFile(self,filename):
        """
        Method for loading a Parameter File
        """
        textEdit = textedit.TextEdit(filename,self)
        textEdit.customDataChanged.connect(self.changeTabName)
        self.activateEssential(textEdit) #Activates QActions and Widgets
        self.tabWidget.show()
        try:
            textEdit.load()
            #textEdit.frTextObject.getText()
            self.index_tabs += 1
        except EnvironmentError as e:
            QMessageBox.warning(self,
                    "G.R.O.M. Editor -- Load Error",
                    "Failed to load {0}: {1}".format(filename, e))
            textEdit.close()
            del textEdit
        else:
            self.tabWidget.addTab(textEdit, textEdit.windowTitle())
            self.tabWidget.setCurrentWidget(textEdit)

    def showParamStuff(self):
        self.tabWidget.show()
        textEdit = textedit.TextEdit(parent = self)
        self.activateEssential(textEdit)
        self.tabWidget.addTab(textEdit, 'Unnamed-%s'%self.index_tabs)
        self.index_tabs += 1
        self.tabWidget.setCurrentWidget(textEdit)
        document = textEdit.document()
        document.clear()
        document.setModified(False)
        self.tabWidget.currentWidget().setFocus()
        self.filename = None
        #self.updateUi()
        self.actionZoom_In.setEnabled(True)
        self.actionZoom_Out.setEnabled(True)

    def customMenuCoord(self,tableWidget):
        self.tableWidget = tableWidget
        tableWidget.setContextMenuPolicy(Qt.CustomContextMenu) #This is absolutely important
        self.verticalHeaders = tableWidget.verticalHeader()
        self.verticalHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeaders.customContextMenuRequested.connect(self.verticalHeader_popup)
        self.horizontalHeaders = tableWidget.horizontalHeader()
        self.horizontalHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeaders.customContextMenuRequested.connect(self.horizontalHeader_popup)
        tableWidget.customContextMenuRequested.connect(self.tableContextMenu)

    def showCoordStuff(self,ModelType):
        self.tabWidget.show()
        tableWidget = tableView.TableEdit(modelType = ModelType,parent = self)
        self.activateEssential(tableWidget)
        self.tabWidget.addTab(tableWidget, 'Unnamed-%s.%s'%(self.index_tabs,ModelType.lower()))
        self.index_tabs += 1
        self.tabWidget.setCurrentWidget(tableWidget)
        tableWidget.setAlternatingRowColors(True)
        self.activateEssential(tableWidget)
        self.customMenuCoord(tableWidget)




    def inactivateEssential(self):
        """
        THis method is used to deactivate,hide  Actions and Widgets
        """
        self.tabWidget.hide()
        self.moreFrame.hide()
        self.actionZoom_In.setEnabled(False)
        self.actionZoom_Out.setEnabled(False)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionPaste.setEnabled(False)
        self.actionAdd_Row.setEnabled(False) #
        self.actionRemove_Row.setEnabled(False)#
        self.actionRemove_Row.setEnabled(False)
        self.actionIconHelp.setEnabled(False)
        self.actionMulti_Rename.setEnabled(False)
        self.actionRenumerate.setEnabled(False)
        self.actionSelect_All.setEnabled(False)
        self.actionDeselect_All.setEnabled(False)
        self.actionFind.setEnabled(False)
        self.actionReplace.setEnabled(False)
        self.actionUndo.setEnabled(False)
        self.actionRedo.setEnabled(False)
        self.actionComment.setEnabled(False)
        self.actionUncomment.setEnabled(False)
        #: This part is new
        self.actionOpen_in_VMD.setEnabled(False)
        self.actionOpen_in_PyMol.setEnabled(False)
        self.actionOpen_in_Avogadro.setEnabled(False)

    def activateEssential(self,currentWidget):
        """
        This method is used to activate Actions and Widgets

        Args:
              currentWidget (QWidget*): reference of the widget Instance

        """
        if currentWidget is None or not isinstance(currentWidget, QPlainTextEdit):
            self.actionZoom_In.setEnabled(False)
            self.actionZoom_Out.setEnabled(False)
            self.actionMulti_Rename.setEnabled(True)
            self.actionRenumerate.setEnabled(True)
            self.actionAdd_Row.setEnabled(True)
            self.actionRemove_Row.setEnabled(True)
            self.actionComment.setEnabled(False)
            self.actionUncomment.setEnabled(False)
            self.actionOpen_in_VMD.setEnabled(True)
            self.actionOpen_in_PyMol.setEnabled(True)
            self.actionOpen_in_Avogadro.setEnabled(True)
        else:
            self.actionZoom_In.setEnabled(True)
            self.actionZoom_Out.setEnabled(True)
            self.actionMulti_Rename.setEnabled(False)
            self.actionRenumerate.setEnabled(False)
            self.actionAdd_Row.setEnabled(False)
            self.actionRemove_Row.setEnabled(False)
            self.actionComment.setEnabled(True)
            self.actionUncomment.setEnabled(True)
            self.actionOpen_in_VMD.setEnabled(False)
            self.actionOpen_in_PyMol.setEnabled(False)
            self.actionOpen_in_Avogadro.setEnabled(False)
        #:------------------------------------------------
        self.actionIconHelp.setEnabled(True)
        self.actionCut.setEnabled(True)
        self.actionCopy.setEnabled(True)
        self.actionPaste.setEnabled(True)
        self.actionSelect_All.setEnabled(True)
        self.actionDeselect_All.setEnabled(True)
        self.actionFind.setEnabled(True)
        self.actionReplace.setEnabled(True)
        self.actionUndo.setEnabled(True)
        self.actionRedo.setEnabled(True)


    def horizontalHeader_popup(self,point):
        """
        Custom horizontal Header Menu for tableWidget
        """
        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.actionCut)
        self.popMenu.addAction(self.actionCopy)
        self.popMenu.addAction(self.actionPaste)
        self.popMenu.addAction(self.actionMulti_Rename) #
        self.popMenu.exec_(self.tableWidget.mapToGlobal(point))


    def verticalHeader_popup(self,point):
        """
        Custom vertical Header Menu for tableWidget
        """
        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.actionCut)
        self.popMenu.addAction(self.actionCopy)
        self.popMenu.addAction(self.actionPaste)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionAdd_Row) #
        self.popMenu.addAction(self.actionRemove_Row)
        self.popMenu.addAction(self.actionMulti_Rename) #
        self.popMenu.exec_(self.tableWidget.mapToGlobal(point))

    def tableContextMenu(self,point):
        """
        Custom context Menu for tableWidget
        """
        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.actionCut)
        self.popMenu.addAction(self.actionCopy)
        self.popMenu.addAction(self.actionPaste)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.actionMulti_Rename) #
        self.popMenu.exec_(self.tableWidget.mapToGlobal(point))



    def cell_was_clicked(self, row, column):
        #print("Row %d and Column %d was clicked" % (row, column))
        item = self.tableWidget.item(row, column)
        self.ID = item.text()
        #print(self.ID)
        #print self.tableWidget.selectedItems()
        #print self.tableWidget.selectedIndexes() #Need to work this out
        for item in self.tableWidget.selectedIndexes():
            print("selectedIndexes", item.row(), item.column())



    def editCopy(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.editCopy()
        except:
            if currentWidget  is None or not isinstance(currentWidget, QPlainTextEdit):
                return
            currentWidget.textCopy()


    def editCut(self):
        print('Cut Cut buddy')
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.editCut()
        except:
            if currentWidget is None or not isinstance(currentWidget, QPlainTextEdit):
                return
            currentWidget.textCut()

    def editPaste(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.editPaste()
        except:
            if currentWidget is None or not isinstance(currentWidget, QPlainTextEdit):
                return
            currentWidget.textPaste()






    def editUndo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.undo()
        except Exception as e:
            print("Problem with undo: ",e)



    def editRedo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.redo()
            self.restoreTextSearch(currentWidget)
        except Exception as e:
            print("Problem with redo: ",e)



    def editSelectAll(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.selectAll()
        except:
            print("Problem with select all")

    def editDeselectAll(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.clearSelection()
        except:
            currentWidget.deselectAll()


    def tableAdd_Row(self):
        """
        Method to add row in tableWidget
        """
        try:
            currentWidget = self.tabWidget.currentWidget()
            rows =  currentWidget.selectionModel().selectedRows() #selectedIndexes()
            currentWidget.AddRow(rows)
        except Exception as error:
            self.showError(error)

    def tableRemove_Row(self):
        """
        Method to remove row in tableWidget
        """
        try:
            currentWidget = self.tabWidget.currentWidget()
            rows =  currentWidget.selectionModel().selectedRows()
            currentWidget.RemoveRow(rows)
        except Exception as error:
            self.showError(error)



    def detectOS(self):
        self.os = platform.system()
        #print('OS: ',self.os)
        if self.os == 'Windows':
            self.fileOpen = "file:///"
        else:
            self.fileOpen = "file://"



    def showHelpMenu(self):
        """
        Method to show Help
        """
        if self.actionIconHelp.isEnabled() == False:
            return
        if self.moreFrame_show == False:
            self.moreFrame.show()
            self.moreFrame.resize(200,400)
            self.splitter.setSizes([300,250])
            self.WebView_place = QWidget()
            self.horizontalLayout = QHBoxLayout(self.WebView_place)
            self.view = QWebView(self.WebView_place)
            self.gridLayout.addWidget(self.view, 1, 0, 1, 2)
            self.comboBox.currentIndexChanged.connect(self.showHTML)
            if self.moreFrame_open  == False:
                place =  self.fileOpen +str(__current_directory__)+ "/documentation/mdp_param_v5/mdp%20options.html"
                self.view.load(QUrl(place))#
            self.moreFrame_show = True
        else:
            self.moreFrame.hide()
            self.moreFrame_show = False

    def findInHelp(self,text): #Buggy need to fix it
        if self.moreFrame_show == False:
            self.showHelpMenu()
        self.view.findText('',QWebPage.HighlightAllOccurrences)
        self.view.findText(text,QWebPage.HighlightAllOccurrences)
        self.view.findText(text,QWebPage.HighlightAllOccurrences)


    def showHTML(self):
        """
        Method to show  HTML help files
        """
        if self.comboBox.currentText() == 'mdp options(v5.0)':
            #print('tada ',str(__current_directory__))
            place = self.fileOpen +str(__current_directory__)+ "/documentation/mdp_param_v5/mdp%20options.html"
            self.view.load(QUrl(place))#
        elif self.comboBox.currentText() == 'mdp options(v4.6)':
            place = self.fileOpen +str(__current_directory__)+ "/documentation/mdp_param_v4.6/mdp%20options.html"
            self.view.load(QUrl(place))#
        else:
            place = self.fileOpen +str(__current_directory__)+ "/documentation/coordinate_file_html/Coordinate%20File%20-%20Gromacs.html"
            self.view.load(QUrl(place))# #this works
        self.moreFrame_open = True


    #: WIP This method hasn't been implemented yet
    def ResNumFix(self):
        QMessageBox.warning(self,"Oops",'Renumerate not yet implemented')


    def MultiRename(self):
        """
        Method for replacing multiple Cells in table Widget
        """
        currentWidget = self.tabWidget.currentWidget()
        if currentWidget is None or  isinstance(currentWidget, QPlainTextEdit):
            return
        try:
            if len(currentWidget.selectedIndexes()) > 0:
                renameOption = MultipleRenameDialog()
                renameOption.show()
                if renameOption.exec_():
                    value = renameOption.RenamelineEdit.text()
                    currentWidget.multi_rename(value)
            else:
                QMessageBox.warning(self,"Oops",'No cells selected,please select at least one')
        except Exception as error:
            self.showError(error)

    def FindReplace(self):
        """
        Method for Find and Replace dialog
        """
        for window in MainWindow.Instances:
                print(window.state)
                if (isAlive(window) and
                    window.state == 'search'):
                    window.activateWindow()
                    window.raise_()
                    break
        else:
                self.dialogFR = findandreplacedlg.FindAndReplaceDlg()
                self.dialogFR.show()
                MainWindow.Instances.add(self.dialogFR)
                MainWindow.Search_Dialog_activated = False
        self.searchToMake()


    def searchToMake(self):
        """
        Method for updating Search Dialog widget's reference with current
        active Widget
        """
        currentWidget = self.tabWidget.currentWidget()
        self.found = False
        self.dialogFR.AddInfo(currentWidget = currentWidget)






def isAlive(qobj):
    """
    Function to check if window is alive
    """
    import sip
    try:
        sip.unwrapinstance(qobj)
    except RuntimeError:
        return False
    return True




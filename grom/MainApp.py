# -*- coding: utf-8 -*-
"""
    GROM.MainApp
    ~~~~~~~~~~~~~

    This is the main program with its GUI

    :copyright: (c) 2014 by Hovakim Grabski.
    :license: GPL, see LICENSE for more details.
"""""

import os
import sys
import platform
from PyQt5.QtCore import (Qt, QFileInfo, QUrl) #QDir new
from PyQt5.QtWidgets import (QMainWindow, QApplication,QWidget, QUndoStack, QFileDialog,QTextEdit, QMessageBox, QHBoxLayout, QMenu)
sys.path.append('ui/')
sys.path.append('documentation/')

import ui_mainWindow as MW #Imports MainWindow GUI


import Icons_rc


import textedit # Imports custom Text Editor
import findandreplacedlg #Imports
import PDB_parse #Imports PDB parse and write module
import PDB_tableview as PDB_Table  #Imports custom TableView widget
from modules import * #Import various modules for Help, MultiRename and Choose Dialog Widgets



#: PyQt for Python 3 doesn't use QString
try:
    from PyQt5.QtCore import QString
except ImportError:
     #we are using Python3 so QString is not defined
    QString = str



__version__ = "0.5-alpha"
__current_directory__ = os.getcwd()



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




        #: Detect OS
        self.detectOS()

        #: disables help Widget
        self.moreFrame_open = False
        self.state = 'editor'
        self.filename = filename
        self.parent = parent

        self.setAttribute(Qt.WA_DeleteOnClose)
        MainWindow.Instances.add(self) #Look in this one


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
        self.tabWidget.blockSignals(False)

        self.tabWidget.currentChanged.connect(self.configureStuff)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.destroyed.connect(MainWindow.updateInstances)
        #----> SIGNALS END

        #: if tab count more than allowed show warning
        if self.tabWidget.count() >  self.tabs_allowed:
            QMessageBox.warning(self,"Oops",'No more tabs are allowed')


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
                self.fileNewCoord()
            self.filename = "Untitled"
        else:
            QMessageBox.warning(self,'App','Dialog Canceled')





    def fileNewParam(self):
        #: This creates new Parameter File(.mdp,.itp,.top)
        #if not self.okToContinue():
            #return
        if self.tabWidget.count() < self.tabs_allowed  :
            self.showParamStuff()
        else:
            QMessageBox.warning(self,"Oops",'No more tabs are allowed')




    def fileNewCoord(self):
        #This creates new Coordinate File(.pdb)
        if self.tabWidget.count() < self.tabs_allowed  :
            self.showCoordStuff()
        else:
            print('Ouch')
            QMessageBox.warning(self,"Oops",'No more tabs are allowed')



    def FileOpen(self):
        """This is for loading file and putting into QTable QTextEditor"""
        #if not self.okToContinue():
            #return
        dir = (os.path.dirname(self.filename)
                if self.filename is not None else ".")
        fname_load = QFileDialog.getOpenFileName(self,
                "G.R.O.M. Editor - Choose File", dir,
                "MD files ( *.pdb *.mdp *.itp *.top)")
        fname = fname_load[0]
        #print('fname is ',fname)
        if 'pdb' not in fname: #Later need to add gro support
                if not len(fname) < 2:
                    for i in range(self.tabWidget.count()):
                        textEdit = self.tabWidget.widget(i)
                        if textEdit.filename == fname:
                            self.tabWidget.setCurrentWidget(textEdit)
                            break
                    else:
                        self.loadParamFile(fname)
        else:
            mol,info_ready = PDB_parse.PDBparse(fname)
            if len(mol[0]) != 12:
                QMessageBox.warning(self,
                "G.R.O.M. Editor -- Load Error",
                "Please check your PDB file, len < 12")
            else:
                self.loadCoordFile(fname)

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
            if  isinstance(currentWidget, QTextEdit):
                try:
                    currentWidget.save()
                    self.tabWidget.setTabText(self.tabWidget.currentIndex(),
                            QFileInfo(currentWidget.filename).fileName())
                    print('save name ',currentWidget.filename)
                    self.statusbar.showMessage('Finished Location: %s' %str(currentWidget.filename))
                    return True
                except EnvironmentError as e:
                    QMessageBox.warning(self,
                            "Tabbed Text Editor -- Save Error",
                            "Failed to save {0}: {1}".format(currentWidget.filename, e))
                    return False
            else:
                try:
                    currentWidget.save()
                    self.statusbar.showMessage('Finished Location: %s' %str(currentWidget.filename))
                except Exception as e:
                    QMessageBox.warning(self,
                            "Tabbed Text Editor -- Save Error",
                            "Failed to save {0}: {1}".format(currentWidget.filename, e))
                    return False
        except Exception as e:
            self.showError(e)


    def fileSaveAs(self): #Half has been achieved
        """
        Method for saving currentWidget's content to File.
        If currentWidget is instance of TextEditor, save to parameter file.
        Else to coordinate File.
        """
        try:
            currentWidget = self.tabWidget.currentWidget()
            if  isinstance(currentWidget, QTextEdit):
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
            self.showError(error)


    def loadCoordFile(self, filename):
        """
        Method for loading a Coordinate File
        """
        tableWidget = PDB_Table.TableEdit(filename)
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


    def loadParamFile(self,filename):
        """
        Method for loading a Parameter File
        """
        textEdit = textedit.TextEdit(filename)
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
        textEdit = textedit.TextEdit()
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

    def showCoordStuff(self):
        self.tabWidget.show()
        tableWidget = PDB_Table.TableEdit()
        self.activateEssential(tableWidget)
        self.tabWidget.addTab(tableWidget, 'Unnamed-%s.pdb'%self.index_tabs)
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


    def activateEssential(self,currentWidget):
        """
        This method is used to activate Actions and Widgets

        Args:
              currentWidget (QWidget*): reference of the widget Instance

        """
        if currentWidget is None or not isinstance(currentWidget, QTextEdit):
            self.actionZoom_In.setEnabled(False)
            self.actionZoom_Out.setEnabled(False)
            self.actionMulti_Rename.setEnabled(True)
            self.actionRenumerate.setEnabled(True)
            self.actionAdd_Row.setEnabled(True)
            self.actionRemove_Row.setEnabled(True)
        else:
            self.actionZoom_In.setEnabled(True)
            self.actionZoom_Out.setEnabled(True)
            self.actionMulti_Rename.setEnabled(False)
            self.actionRenumerate.setEnabled(False)
            self.actionAdd_Row.setEnabled(False)
            self.actionRemove_Row.setEnabled(False)
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
            if currentWidget  is None or not isinstance(currentWidget, QTextEdit):
                return
            cursor = currentWidget.textCursor()
            text = cursor.selectedText()
            if not text == '':
                clipboard = QApplication.clipboard()
                clipboard.setText(text)



    def editCut(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.editCut()
        except:
            if currentWidget is None or not isinstance(currentWidget, QTextEdit):
                return
            cursor = currentWidget.textCursor()
            text = cursor.selectedText()
            if not len(text)<1:
                cursor.removeSelectedText()
                clipboard = QApplication.clipboard()
                clipboard.setText(text)


    def editPaste(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.editPaste()
        except:
            if currentWidget is None or not isinstance(currentWidget, QTextEdit):
                return
            clipboard = QApplication.clipboard()
            currentWidget.insertPlainText(clipboard.text())






    def editUndo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.undo()
        except:
            print("Problem with undo")

    def editRedo(self):
        currentWidget = self.tabWidget.currentWidget()
        currentWidget.setFocus()
        try:
            currentWidget.redo()
        except:
            print("Problem with redo")


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
            cursor = currentWidget.textCursor()
            cursor.movePosition( QTextCursor.End )
            currentWidget.setTextCursor( cursor )


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
        if self.state == 'coord':
            self.tableWidget.ResNumFixer()
            if len(self.tableWidget.selectedIndexes()) > 0:
                renameOption = MultipleRenameDialog()
                renameOption.RnameLabel.setText('Fix ResNum')
                if renameOption.exec_():
                    print('TADA ResNumFix working for now')
                    value = renameOption.RenamelineEdit.text()
        else:
                QMessageBox.warning(self,"Oops",'Renumerate not yet implemented')


    def MultiRename(self):
        """
        Method for replacing multiple Cells in table Widget
        """
        currentWidget = self.tabWidget.currentWidget()
        try:
            if len(currentWidget.selectedIndexes()) > 0:
                renameOption = MultipleRenameDialog()
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




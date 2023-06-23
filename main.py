################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import subprocess, os, glob

# GUI FILE
from app_modules import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        ########################################################################
        ## START - WINDOW ATTRIBUTES
        ########################################################################

        ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle('OLC MISEQHASHR')
        UIFunctions.labelTitle(self, 'OLC MISEQHASHR')
        UIFunctions.labelDescription(self, '')
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## ==> CREATE MENUS
        ########################################################################

        ## ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        ## ==> END ##

        ## ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "HOME", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "HASH", "btn_analyze", "url(:/16x16/icons/16x16/cil-folder-open.png)", True)
        UIFunctions.addNewMenu(self, "Examine Table", "btn_examine_table", "url(:/16x16/icons/16x16/cil-chart.png)", True)
        UIFunctions.addNewMenu(self, "About", "btn_widgets", "url(:/16x16/icons/16x16/cil-people.png)", False)
        ## ==> END ##

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_home")
        ## ==> END ##

        ## ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        ## ==> END ##

        ## USER ICON ==> SHOW HIDE
        #UIFunctions.userIcon(self, "", "url(:/24x24/icons/24x24/confindrlogo.png)", True)
        ## ==> END ##


        ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##

        ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##

        ########################################################################
        ## END - WINDOW ATTRIBUTES
        ############################## ---/--/--- ##############################




        ########################################################################
        #                                                                      #
        ## START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##

        # Firstly, defines all widgets used
        self.widgetDefiner()

        # Then, calls each function according to each button clicked
        self.sequenceBtn.clicked.connect(self.analyzeClicker)

        ########################################################################

        ########################################################################
        #                                                                      #
        ## END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- ##
        #                                                                      #
        ############################## ---/--/--- ##############################


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    
    # Function for when the button in analyzation station is clicked
    def analyzeClicker(self):

        # Gets the name of the folder with the data
        folderName = str(QFileDialog.getExistingDirectory(self, "Select Path to MiSeq Run"))
        print("This is the folder directory: " + folderName)

        # Checks if the folder selected contains any fastq.gz or fasta files which is what the hasher uses. If not, return that dummy back
        if glob.glob(f'{folderName}/*.fastq.gz') or glob.glob(f'{folderName}/*.fasta'):

            # Prints a success message to say the file is found
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Successfully found folder. Results may take up to 5 minutes to complete")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

            # Checks what options are selected and applies those arguements to our command line
            versionDisplay = self.versionOptions()
            verbosity = self.verbosityOptions()

            # Uses the folder name as an argument to run ConFindr and get the results. Mem represents total allocated memory that is being reserved for confindr
            self.test_out = os.path.join(folderName, "test_out")
            subprocess.run(f'MiSeqHashR -f {folderName}{versionDisplay}{verbosity}')
            print(f'MiSeqHashR -f {folderName}{versionDisplay}{verbosity}')

            # Prints a success message to say the results are successfully completed
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Successfully hashed file!")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()


        # Checks if there is a folder containing your sequence or if there is anything written
        elif len(folderName) == 0:
            self.analyzeLabelError.setText("Please select a folder to continue")

        else:
            self.analyzeLabelError.setText("The folder does not contain any fastq.gz or fasta files")        

    # Buttons that take you to different pages in stacked widget
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE ANALYZE
        if btnWidget.objectName() == "btn_analyze":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_analysis)
            UIFunctions.resetStyle(self, "btn_analyze")
            UIFunctions.labelPage(self, "Hash")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE EXAMINE
        if btnWidget.objectName() == "btn_examine_table":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_table)
            UIFunctions.resetStyle(self, "btn_examine_table")
            UIFunctions.labelPage(self, "Examine Table")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "About")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
    ## ==> END ##

    ########################################################################
    ## END ==> APP EVENTS
    ############################## ---/--/--- ##############################

    def widgetDefiner(self):
        # Defines all the widgets used [there is a lot of them]
        self.sequenceBtn = self.findChild(QPushButton, "sequenceBtn")
        self.analyzeLabelError = self.findChild(QLabel, "analyzeLabelError")

        # Advanced arguements
        self.versionCheckBox = self.findChild(QCheckBox, "versionCheckBox")
        self.verbosityDropdownMenu = self.findChild(QComboBox, "verbosityDropdownMenu")        

#---------------------------Argument Functions----------------------------------------------

    # Checks if the version option is selected
    def versionOptions(self):
        if self.versionCheckBox.isChecked() == True:
            option = ' --version'
        else:
            option = ''
        return option  

    # Checks if you chose Debug, Info or Warning as the amount of output on your screen
    def verbosityOptions(self):
        if self.verbosityDropdownMenu.currentText() == 'Debug':
            option = ' -v debug'
        elif self.verbosityDropdownMenu.currentText() == 'Info':
            option = ' -v info'
        elif self.verbosityDropdownMenu.currentText() == 'Error':
            option = ' -v error'
        elif self.verbosityDropdownMenu.currentText() == 'Critical':
            option = ' -v critical'
        else:
            option = ' -v warning'
        return option  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())

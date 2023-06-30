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
import subprocess, os, glob, time, datetime, requests, urllib3

# GUI FILE
from app_modules import *

# Establish API_ENDPOINT to connect to Foodport
API_ENDPOINT = 'https://10.148.57.4/api/'

# SSL cert isn't quite right on portal. Use this to disable warning.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        UIFunctions.addNewMenu(self, "UPLOAD", "btn_upload", "url(:/16x16/icons/16x16/cil-cloud-upload.png)", True)
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

        appIcon = QIcon("MiSeqHashRIcon.png")
        self.setWindowIcon(appIcon)


        ########################################################################
        #                                                                      #
        ## START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##

        # Firstly, defines all widgets used
        self.widgetDefiner()

        # Then, calls each function according to each button clicked
        self.sequenceBtn.clicked.connect(self.analyzeClicker)
        self.uploadBtn.clicked.connect(self.uploadClicker)

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
        miSeqFolderName = os.path.join(folderName, 'Data', 'Intensities', 'BaseCalls')
        print("This is the folder directory: " + folderName)

        # Checks if the folder selected contains any fastq.gz files which is what the hasher uses. Also checks if it contains the correct format for a miSeq Folder.
        if os.path.exists(miSeqFolderName):

            # Gets number of fastq files
            numberOfFastQ=len(glob.glob(os.path.join(miSeqFolderName, '*fastq.gz')))

            if numberOfFastQ:

                # Prints a success message to say the file is found
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Successfully found folder. Hashing files now.")
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()
                
                # Gets the size of the file to determine how long the loading bar will take
                size = 0
                for path, dirs, files in os.walk(miSeqFolderName):
                    for f in files:
                        fp = os.path.join(path, f)
                        size += os.path.getsize(fp)

                print('The size of the file is: ' + str(size))

                # Resets error message
                self.analyzeLabelError.setText("")


                # Adding the loading bar widget to our window
                self.progressBar.setMinimum(0)
                self.progressBar.setMaximum(100)

                # Uses the folder name as an argument to run miSeqHashR and get the results.
                self.test_out = os.path.join(folderName, "test_out")
                p = subprocess.Popen(f'MiSeqHashR -f {folderName}', shell=True)

                # Runs the loading bar as miSeqHashR is running
                while p.poll() is None:
                    # Runs the progress bar based on the size of the file
                    
                    numberOfHashes=len(glob.glob(os.path.join(folderName, 'hashes', '*.txt')))
                    progress=int((numberOfHashes/numberOfFastQ)*100)
                    self.progressBar.setValue(progress)
                    time.sleep(1)

                self.progressBar.setValue(100)

                # Prints a success message to say the results are successfully completed
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Successfully hashed files!")
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()
            
            else:
                self.analyzeLabelError.setText("The directory doesn't contain any fastq.gz files")


        # Checks if there is a folder containing your sequence or if there is anything written
        elif len(folderName) == 0:
            self.analyzeLabelError.setText("Please select a folder to continue")

        else:
            self.analyzeLabelError.setText("The folder does not contain the MiSeq file structure")        

    def uploadClicker(self):
        # Gets the name of the folder with the data
        folderName = str(QFileDialog.getExistingDirectory(self, "Select Path to MiSeq Run"))
        miSeqFolderName = os.path.join(folderName, 'Data', 'Intensities', 'BaseCalls')
        print("This is the folder directory: " + folderName)

        # Checks if the folder selected contains any fastq.gz files which is what the hasher uses. Also checks if it contains the correct format for a miSeq Folder.
        if os.path.exists(miSeqFolderName):

            # Gets number of fastq files
            numberOfFastQ=len(glob.glob(os.path.join(miSeqFolderName, '*fastq.gz')))

            # If there exists fastq files
            if numberOfFastQ:

                # Prints a success message to say the file is found
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Successfully found folder. Checking credentials.")
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()

                # Will kick user out if credentials are wrong. Should get this somewhat more elegant in the future.
                self.check_credentials(self.emailField, self.passwordField)

                # Prints a success message when credentials are accepted
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Successfully accepted credentials. Folder is now being checked for hashing.")
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()

                # Constantly checks if any hashing is going on
                while True:
                    print('Checking for runs that haven\'t been uploaded.')
                    run_folders = [x[0] for x in os.walk(folderName)]
                    if folderName in run_folders:
                        run_folders.remove(folderName)
                    for run_folder in run_folders:
                        run_exists = self.check_run_exists_in_portal(run_folder, self.emailField, self.passwordField)
                        if run_exists is False:
                            print('Found new run to upload! Starting upload of {}'.format(run_folder))
                            self.upload_run(run_folder, self.emailField, self.passwordField)
                    time.sleep(1800)

            else:
                self.analyzeLabelError.setText("The directory doesn't contain any fastq.gz files")

        # Checks if there is a folder containing your sequence or if there is anything written
        elif len(folderName) == 0:
            self.analyzeLabelError.setText("Please select a folder to continue")

        else:
            self.analyzeLabelError.setText("The folder does not contain the MiSeq file structure")    

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

        # PAGE UPLOAD
        if btnWidget.objectName() == "btn_upload":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_upload)
            UIFunctions.resetStyle(self, "btn_upload")
            UIFunctions.labelPage(self, "Upload")
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
        # Defines progress bar
        self.progressBar = self.findChild(QProgressBar, "progressBar")

        # Defines all the widgets used 
        self.sequenceBtn = self.findChild(QPushButton, "sequenceBtn")
        self.analyzeLabelError = self.findChild(QLabel, "analyzeLabelError")   
        self.uploadBtn = self.findChild(QPushButton, "uploadBtn")
        self.emailField = self.findChild(QLineEdit, "emailInput")   
        self.passwordField = self.findChild(QLineEdit, "passwordInput")  

    ########################################################################
    ## auto_run_uploader.py functions
    ############################## ---/--/--- ##############################
    def check_credentials(self, email, password):
        # Try to access an API endpoint that's password protected.
        response = requests.get(API_ENDPOINT + 'run_cowbat/totally_fake_run_name', auth=(email, password), verify=False)
        if response.status_code == 403:
            raise ValueError('Your username or password is incorrect! Close the application and try again.')


    def wait_for_run_completion(self, run_folder):
        # Once GenerateFASTQRunStatistics is created the run has completed. Check status every 20 minutes until run
        # completion.
        run_complete = False
        while run_complete is False:
            if os.path.isfile(os.path.join(run_folder, 'GenerateFASTQRunStatistics.xml')):
                run_complete = True
            else:
                print('{}: Sequencing run not yet complete. Will check again in 20 minutes...'.format(datetime.datetime.now()))
                time.sleep(1200)

        # Sleep for a few minutes once everything finishes just so we're super duper sure that all files are created.
        time.sleep(120)


    def upload_files_and_start_run(self, run_folder, email_address, password):
        x = os.path.split(run_folder)[1].split('_')
        run_name = x[0] + '_' + x[1]
        metadata_files = ['CompletedJobInfo.xml', 'GenerateFASTQRunStatistics.xml', 'RunInfo.xml', 'runParameters.xml',
                        'SampleSheet.csv']
        config_xml = os.path.join(run_folder, 'Data', 'Intensities', 'BaseCalls', 'config.xml')
        interop_files = sorted(glob.glob(os.path.join(run_folder, 'InterOp', '*.bin')))
        sequence_files = sorted(glob.glob(os.path.join(run_folder, 'Data', 'Intensities', 'BaseCalls', '*.fastq.gz')))

        all_uploaded_successfully = True

        # Upload metadata files.
        for metadata_file in metadata_files:
            # Check if file already exists, don't want to bother re-uploading if it does.
            response = requests.get(API_ENDPOINT + 'upload/{}/{}'.format(run_name, metadata_file),
                                    auth=(email_address, password),
                                    verify=False)
            response_dict = response.json()
            if response_dict['exists'] is False or response_dict['size'] == 0:
                with open(os.path.join(run_folder, metadata_file), 'rb') as data:
                    response = requests.put(API_ENDPOINT + 'upload/{}/{}'.format(run_name, metadata_file),
                                            data=data,
                                            auth=(email_address, password),
                                            verify=False)
                    if response.status_code == 204:
                        print('{}: Successfully uploaded {}'.format(datetime.datetime.now(), metadata_file))
                    else:
                        all_uploaded_successfully = False

        # Upload config.xml
        response = requests.get(API_ENDPOINT + 'upload/{}/{}'.format(run_name, os.path.split(config_xml)[1]),
                                auth=(email_address, password),
                                verify=False)
        response_dict = response.json()
        if response_dict['exists'] is False or response_dict['size'] == 0:
            with open(config_xml, 'rb') as data:
                response = requests.put(API_ENDPOINT + 'upload/{}/{}'.format(run_name, os.path.split(config_xml)[1]),
                                        data=data,
                                        auth=(email_address, password),
                                        verify=False)
                if response.status_code == 204:
                    print('{}: Successfully uploaded config.xml'.format(datetime.datetime.now()))
                else:
                    all_uploaded_successfully = False

        # InterOp files
        for interop_file in interop_files:
            response = requests.get(API_ENDPOINT + 'upload/{}/{}'.format(run_name, os.path.split(interop_file)[1]),
                                    auth=(email_address, password),
                                    verify=False)
            response_dict = response.json()
            if response_dict['exists'] is False or response_dict['size'] == 0:
                with open(interop_file, 'rb') as data:
                    response = requests.put(API_ENDPOINT + 'upload/{}/{}'.format(run_name, os.path.split(interop_file)[1]),
                                            data=data,
                                            auth=(email_address, password),
                                            verify=False)
                    if response.status_code == 204:
                        print('{}: Successfully uploaded {}'.format(datetime.datetime.now(), interop_file))
                    else:
                        all_uploaded_successfully = False

        # Sequence files.
        for sequence_file in sequence_files:
            response = requests.get(API_ENDPOINT + 'upload/{}/{}'.format(run_name, os.path.split(sequence_file)[1]),
                                    auth=(email_address, password),
                                    verify=False)
            response_dict = response.json()
            if response_dict['exists'] is False or response_dict['size'] == 0:
                with open(sequence_file, 'rb') as data:
                    response = requests.put(API_ENDPOINT + 'upload/{}/{}'.format(run_name, os.path.split(sequence_file)[1]),
                                            data=data,
                                            auth=(email_address, password),
                                            verify=False)
                    if response.status_code == 204:
                        print('{}: Successfully uploaded {}'.format(datetime.datetime.now(), sequence_file))
                    else:
                        all_uploaded_successfully = False

        if all_uploaded_successfully:
            # Now start the run actually going
            requests.get(API_ENDPOINT + 'run_cowbat/{}'.format(run_name),
                        auth=(email_address, password),
                        verify=False)
            return True
        else:
            return False


    def upload_run(self, run_folder, email_address, password):
        self.wait_for_run_completion(run_folder)
        attempted_uploads = 0
        successful_upload = False
        while attempted_uploads < 5 and successful_upload is False:
            successful_upload = self.upload_files_and_start_run(run_folder, email_address, password)
            attempted_uploads += 1
        if successful_upload:
            print('Complete!')
        else:
            print('Something went wrong uploading files. You\'ll have to upload them manually.')


    def check_run_exists_in_portal(self, run_folder, email, password):
        x = os.path.split(run_folder)[1].split('_')
        run_name = x[0] + '_' + x[1]
        response = requests.get(API_ENDPOINT + 'run_cowbat/{}'.format(run_name),
                                auth=(email, password),
                                verify=False)
        if response.status_code == 404:
            return False
        elif 'status' in response.json():
            if 'Did not start' in response.json()['status']:
                return True
            else:
                return False
        else:
            return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())
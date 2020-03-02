from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, Qt,QBasicTimer, QPoint
from PyQt5.QtWidgets import (QApplication,QDesktopWidget, QMainWindow)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import traceback, sys
from addDurations import getFileDuration
import math
import ntpath
from shutil import copyfile
import os
# import webbrowser



#Qthread classes
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs

        # self.kwargs = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Ui_MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("MainWindow")
        self.resize(710, 528)
        self.setMouseTracking(True)
        self.setStyleSheet("QMainWindow{\n"
        "    Background: rgb(37, 37, 37);\n"
        "    max-width: 710px;\n"
        "    min-width: 710px;\n"
        "    max-height: 528px;\n"
        "    min-height: 528px;\n"
        "}\n"
        "")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 30, 200, 73))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setStyleSheet("QPushButton{\n"
        "    margin:3px;\n"
        "    border:none;\n"
        "    border-radius: 17px;\n"
        "    background-color: rgb(242, 149, 28);\n"
        "    color: black;\n"
        "    font-size: 15px;\n"
        "    font-family:\"Roboto Black\";\n"
        "    height: 35px;\n"
        "    width: 90px;\n"
        "    font-weight: bolder;\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "     background-color: rgb(235, 189, 101);\n"
        "}")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
        "    margin:3px;\n"
        "    border:none;\n"
        "    border-radius: 17px;\n"
        "    background-color: rgb(242, 149, 28);\n"
        "    color: black;\n"
        "    font-size: 14px;\n"
        "    font-family:\"Roboto Black\";\n"
        "    height: 35px;\n"
        "    width: 90px;\n"
        "    font-weight: bolder;\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "     background-color: rgb(235, 189, 101);\n"
        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setStyleSheet("QLabel{\n"
        "    color:rgb(140, 140, 140);\n"
        "    font-family: \"Roboto Black\";\n"
        "    font-size: 15px;\n"
        "    margin: 0px;\n"
        "}")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 2, 1)
        self.label.raise_()
        self.pushButton_2.raise_()
        self.pushButton.raise_()
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 472, 111, 51))
        self.pushButton_3.setStyleSheet("QPushButton{\n"
        "    margin:3px;\n"
        "    border:none;\n"
        "    border-radius: 22px;\n"
        "    background-color: rgb(242, 149, 28);\n"
        "    color: black;\n"
        "    font-size: 16px;\n"
        "    font-family:\"Roboto Black\";\n"
        "    height: 35px;\n"
        "    width: 90px;\n"
        "    font-weight: bolder;\n"
        "}\n"
        "\n"
"QPushButton:pressed {\n"
"     background-color: rgb(235, 189, 101);\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.threadpool = QThreadPool()
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(590, 472, 111, 51))
        self.pushButton_4.setStyleSheet("QPushButton{\n"
        "    margin:3px;\n"
        "    border:none;\n"
        "    border-radius: 22px;\n"
        "    background-color: rgb(242, 149, 28);\n"
        "    color: black;\n"
        "    font-size: 19px;\n"
        "    font-family:\"Roboto Black\";\n"
        "    height: 35px;\n"
        "    width: 90px;\n"
        "    font-weight: bolder;\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "     background-color: rgb(235, 189, 101);\n"
        "}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(97, 273, 521, 7))
        self.progressBar.setStyleSheet("QProgressBar::chunk{\n"
        "    color:yellow;\n"
        "    background-color: rgb(248, 163, 109);\n"
        "}\n"
        "QProgressBar{\n"
        "    border: none;\n"
        "    background-color: rgb(37, 37, 37);\n"
        "    max-height: 7px;\n"
        "}")
        # self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(116, 300, 491, 16))
        self.label_2.setStyleSheet("QLabel{\n"
        "    color:rgb(210, 210, 210);\n"
        "    font-family: \"Roboto\";\n"
        "    font-size: 15px;\n"
        "    margin: 0px;\n"
        "}")
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 320, 501, 71))
        self.label_3.setStyleSheet("QLabel{\n"
        "    color:rgb(220, 220, 220);\n"
        "    font-family: \"Roboto Black\";\n"
        "    font-size: 15px;\n"
        "    margin: 0px;\n"
        "}")
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(100, 250, 300, 25))
        self.label_4.setStyleSheet("QLabel{\n"
        "    color:rgb(210, 210, 210);\n"
        "    font-family: \"Roboto\";\n"
        "    font-size: 13px;\n"
        "    margin: 0px;\n"
        "}")
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 110, 561, 21))
        self.label_5.setStyleSheet("QLabel{\n"
        "    color:rgb(210, 210, 210);\n"
        "    font-family: \"Roboto\";\n"
        "    font-size: 13px;\n"
        "    margin: 0px;\n"
        "}")
        self.label_5.setObjectName("label_5")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(620, 0, 92, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_6.setStyleSheet("QPushButton{\n"
        "    max-width:35px;\n"
        "    min-width:35px;\n"
        "    max-height:28px;\n"
        "    min-height:28px;\n"
        "    Background: rgb(37, 37, 37);\n"
        "    border:none;\n"
        "}\n"
        "QPushButton:hover {\n"
        "     background-color: rgb(50, 50, 50);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "     background-color: rgb(60, 60, 60);\n"
        "}")
        self.pushButton_6.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/mini.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setStyleSheet("QPushButton{\n"
        "    max-width:35px;\n"
        "    min-width:35px;\n"
        "    max-height:28px;\n"
        "    min-height:28px;\n"
        "    Background: rgb(37, 37, 37);\n"
        "    border:none;\n"
        "}\n"
        "QPushButton:hover {\n"
        "     background-color: rgb(229, 17, 39);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "     background-color: rgb(242, 112, 122);\n"
        "}")
        self.pushButton_5.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/esc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.pushButton_7.setStyleSheet("QPushButton{\n"
        "    Background: rgb(37, 37, 37);\n"
        "    border:none;\n"
        "}\n"
        "QPushButton:hover {\n"
        "}\n"
        "QPushButton:pressed {\n"
        "}")
        self.pushButton_7.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./icons/small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.pushButton_7.setIcon(icon2)
        self.pushButton_7.setIconSize(QtCore.QSize(21, 21))
        self.pushButton_7.setObjectName("pushButton_7")


        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.pushButton_6.clicked.connect(self.showMinimized)
        self.pushButton_5.clicked.connect(self.close)


        self.pushButton_4.clicked.connect(self.threadBoss)
        self.pushButton_4.setDisabled(True)

        self.pushButton_2.clicked.connect(self.selectFolder)
        self.pushButton.clicked.connect(self.selectFile)

        self.pushButton_3.clicked.connect(self.openSourceUrl)


        self.removeFilesInAfolder(r'.\VideosToAnalyze')

        self.pushButton_7.clicked.connect(self.returnNothing)


        self.show()
    def returnNothing(self):
        return

    def openSourceUrl(self):
        import webbrowser
        webbrowser.open('https://github.com/HomamShami/Subtytor')

    def threadBoss(self):
        worker = Worker(lambda : self.gooSubtytor(self.whereToLook))  # Any other args, kwargs are passed to the run function
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)
    def threadBossFolderCopier(self, folder):
        worker = Worker(lambda : self.copyFolderContent(folder))  # Any other args, kwargs are passed to the run function
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def threadBossFileCopier(self, file):
        worker = Worker(lambda : self.copyFile(file))  # Any other args, kwargs are passed to the run function
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    whereToLook = ''
    def selectFolder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select a Folder"))
        # print(folder)
        self.whereToLook = folder
        self.threadBossFolderCopier(folder)

    def copyFolderContent(self, folder):
        self.removeFilesInAfolder(r'.\VideosToAnalyze')
        self.label_5.setText('All Files in: ' + folder)
        self.label_4.setText('Copying Files To Temporary Folder..')
        from distutils.dir_util import copy_tree
        dst = './VideosToAnalyze'
        copy_tree(folder, dst)
        self.pushButton_4.setDisabled(False)
        self.label_4.setText('Done! You can press "Start" now.')


    def selectFile(self):
        import shutil
        filter = "Supported Extensions(*.mp4 *.m4v *.m4a *.wav)"
        folder = QFileDialog.getOpenFileName(self, "Select a File",'',filter)
        filefolder = folder[0]
        filename=ntpath.basename(filefolder)
        filePathWithoutFileName = filefolder[:- len(filename)-1 ]
        # print(filefolder) #file path
        # print(filename) #filename
        # print(filePathWithoutFileName)
        self.whereToLook = filePathWithoutFileName
        self.threadBossFileCopier(filefolder)

    def copyFile(self, filefolder):
        import shutil
        self.label_5.setText(filefolder)
        self.removeFilesInAfolder(r'.\VideosToAnalyze')
        self.label_4.setText('Copying File To Temporary Folder..')
        destination = r'.\VideosToAnalyze'
        shutil.copy2(filefolder, destination)
        self.pushButton_4.setDisabled(False)
        self.label_4.setText('Done! You can press "Start" now.')

    def removeFilesInAfolder(self, targetFolderPath):
        for the_file in os.listdir(targetFolderPath):
            file_path = os.path.join(targetFolderPath, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as ee:
                return
                # print(ee)


    def gooSubtytor(self, hierarchyFolder):
        import time
        import speech_recognition as sr
        from os import path
        import datetime
        import os
        from pathlib import Path
        import subprocess
        import shutil
        from distutils.dir_util import copy_tree
        from requests.exceptions import ProxyError
        from http.client import IncompleteRead
        from detectBestSilenceDuration import goAmadeus
        from convertMilliToTimeString import convertMillisecsToTimeString
        from convertMilliToTimeString import makeBetterEndingTime


        whereToLookToMatchHierarchy = hierarchyFolder # folder you got the videos from

        # print(whereToLookToMatchHierarchy)

        lang = 'en'  # more at:  http://stackoverflow.com/a/14302134
        silenceModifier = 0  # Percent, You Can Enter Minus Values As Well..

        self.progressBar.setProperty("value", 0)

        self.label_2.setText('Time')
        self.label_3.setText('Output')

        self.pushButton_4.setDisabled(True)

        def get_project_root():
            """Returns project root folder."""
            return Path(__file__).parent

        # Test Short Videos In H:/TestVideos

        rootdir = str(get_project_root()) + r'\toAnalyse\SplittedFiles'
        sourceVideosFolder = str(get_project_root()) + r'\VideosToAnalyze'
        temporaryWavFolder = str(get_project_root()) + r'\toAnalyse\wavFiles'
        outputSubtitlesFolder = str(get_project_root()) + r'\outputSubtitles'
        temporarySubtitles = str(get_project_root()) + r'\temporarySubtitles'
        FinishedSubtitles = str(get_project_root()) + r'\FinishedSubtitles'
        archiveFolder = str(get_project_root()) + r'\archiveFolder'


        checkDir = os.listdir(sourceVideosFolder)

        # Checking if the list is empty or not
        if len(checkDir) == 0:
            self.label_4.setText('Please select a File/Folder !')
            sys.exit('nothing to analyze')



        global block_num
        block_num = 0

        ii = 1
        global aa
        aa = 0

        def removeFilesInAfolder(targetFolderPath):
            for the_file in os.listdir(targetFolderPath):
                file_path = os.path.join(targetFolderPath, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as ee:
                    return
                    # print(ee)

        if not os.path.exists(rootdir):
            os.makedirs(rootdir)
        shutil.rmtree(rootdir)
        if not os.path.exists(rootdir):
            os.makedirs(rootdir)

        removeFilesInAfolder(temporaryWavFolder)
        removeFilesInAfolder(outputSubtitlesFolder)
        removeFilesInAfolder(FinishedSubtitles)

        for fname in os.listdir(sourceVideosFolder):
            if fname.endswith(".srt"):
                filuname = os.path.join(sourceVideosFolder, fname)
                os.remove(filuname)

        for fname in os.listdir(sourceVideosFolder):
            if fname.endswith(".mp4") or fname.endswith(".m4v") or fname.endswith(".m4a") or fname.endswith(".wav"):

                input = sourceVideosFolder + r'\%s' % (str(fname))

                newName = fname.replace(" ", "-s-")
                newNameX = newName.replace("&", "-a-")

                inputNamee = sourceVideosFolder + r'\%s' % (newNameX)
                ouputNamee = temporaryWavFolder + r'\%s' % (newNameX) + '.wav'

                os.rename(input, inputNamee)

                DEVNULL = subprocess.DEVNULL
                command = "ffmpeg -i %s -ab 160k -ac 1 -ar 16000 -vn %s -f wav" % (inputNamee, ouputNamee)
                # subprocess.call(command, shell=False)
                output = subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

        myList = []
        for fname in os.listdir(temporaryWavFolder):

            if fname.endswith(".wav"):

                ffname = fname[:-4]

                newFolder = str(get_project_root()) + r'\toAnalyse\SplittedFiles\%s' % (ffname)
                if not os.path.exists(newFolder):
                    os.makedirs(newFolder)
                fname = temporaryWavFolder + '\%s' % (fname)

                self.label_4.setText('Analyzing..')
                newData = goAmadeus(fname, newFolder, silenceModifier)
                myList.append(newData)

        for directory, dirs, files in os.walk(rootdir):
            self.label_4.setText('Processing..')
            try:
                block_num = 1
                aa = 0
                # print(directory)

                for filename in os.listdir(directory):
                    mVideo = temporaryWavFolder +'\%s'%os.listdir(temporaryWavFolder)[ii-1]
                    mVideoDuration = getFileDuration(mVideo)
                    def writeToSrt(giveItToMe):

                        start_time = datetime.datetime(100, 1, 1, 0, 0, 0)

                        def speech_to_srt(current_time, block):

                            global block_num
                            block_num += 1

                            block_str = str(block)

                            global srtFileName
                            if ii >= 0 and ii <= 9:
                                srtFileName = '00000' + str(ii) + "-mySrt.srt"
                            if ii >= 10 and ii <= 99:
                                srtFileName = '0000' + str(ii) + "-mySrt.srt"
                            if ii >= 100 and ii <= 999:
                                srtFileName = '000' + str(ii) + "-mySrt.srt"
                            if ii >= 1000 and ii <= 9999:
                                srtFileName = '00' + str(ii) + "-mySrt.srt"
                            if ii >= 10000 and ii <= 99999:
                                srtFileName = '0' + str(ii) + "-mySrt.srt"

                            current_start_time_new = convertMillisecsToTimeString(myList[ii][block - 1][0])
                            try:
                                current_end_time_new = makeBetterEndingTime(myList[ii][block - 1][1],myList[ii][block][0])
                            except:
                                current_end_time_new = convertMillisecsToTimeString(myList[ii][block - 1][1])

                            xxx = outputSubtitlesFolder + '\%s' % (srtFileName)


                            end = round(int(myList[ii][block - 1][1]/1000))
                            allDu = round(int(mVideoDuration))
                            percento = end/allDu * 100
                            percento = math.ceil(percento)
                            # print(percento)
                            # self.progressBar.setValue(percento)
                            self.progressBar.setProperty("value", percento)
                            self.label_4.setText('Processing.. ('+str(percento)+'%)')

                            with open(xxx, "a", encoding='utf-8') as f:
                                f.write(block_str)
                                f.write("\n")
                                f.write(current_start_time_new)
                                f.write(" --> ")
                                f.write(current_end_time_new)
                                f.write("\n")
                                f.write(giveItToMe)
                                f.write("\n")
                                f.write("\n")

                            self.label_2.setText(str(current_start_time_new) + ' --> ' + str(current_end_time_new))
                            self.label_3.setText(giveItToMe)

                        speech_to_srt(start_time, block_num)

                    # print(filename)
                    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), directory + r'\%s' % (filename))

                    # use the audio file as the audio source
                    r = sr.Recognizer()
                    with sr.AudioFile(AUDIO_FILE) as source:
                        audio = r.record(source)  # read the entire audio file

                    def tryagain2():
                        try:
                            # print("Started")
                            result = r.recognize_google(audio, language=lang)
                            # print('\n')
                            writeToSrt(result)
                            global aa
                            aa += 1

                        except sr.UnknownValueError:
                            # print("could not understand audio.. ")
                            result = ' '
                            writeToSrt(result)
                            aa += 1
                        except sr.RequestError as e:
                            # print("error; {0}".format(e))
                            # print("could not understand audio whatsoever")
                            result = ' '
                            writeToSrt(result)
                        except ConnectionError as a:
                            # print("error; {0}".format(a))
                            # print("CONNECTION ERROR, Trying Again..")
                            time.sleep(3)
                            tryagain2()
                        except RecursionError as b:
                            return
                            # print("Recursive error; {0}".format(b))
                            # print("Couldn't Do It Whatsoever".format(b))
                        except ProxyError as zz:
                            # print(
                            #     "Proxy Error error Occured, Please Change Your Ip To Continue Translation..; {0}".format(
                            #         zz))
                            time.sleep(3)
                            tryagain2()
                        except IncompleteRead as ohGodWhy:
                            # print(
                            #     "Incomplete Read Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         ohGodWhy))
                            time.sleep(3)
                            tryagain2()
                        except ValueError as ohGodWhyy:
                            # print(
                            #     "Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         ohGodWhyy))
                            time.sleep(3)
                            tryagain2()
                        except TimeoutError as stopIt:
                            # print(
                            #     "Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         stopIt))
                            time.sleep(3)
                            tryagain2()
                        except:
                            # print(
                            #     "Unknown Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; ")
                            time.sleep(3)
                            tryagain2()

                    def tryagain1():
                        try:
                            # print("Started")
                            result = r.recognize_google(audio, language=lang)
                            # print('\n')
                            writeToSrt(result)
                            global aa
                            aa += 1

                        except sr.UnknownValueError:
                            # print("could not understand audio")
                            # print(2)
                            # tryagain2()
                            # print("could not understand audio.. ")
                            result = ' '
                            writeToSrt(result)
                            aa += 1
                        except sr.RequestError as e:
                            # print("could not understand audio ".format(e))
                            # print("trying again")
                            time.sleep(3)
                            tryagain2()
                        except ConnectionError as a:
                            # print("error; {0}".format(a))
                            # print("CONNECTION ERROR, Trying Again..")
                            time.sleep(3)
                            tryagain1()
                        except RecursionError as b:
                            # print("Recursive error; {0}".format(b))
                            time.sleep(3)
                            tryagain2()
                        except ProxyError as zz:
                            # print(
                            #     "Proxy Error error Occured, Please Change Your Ip To Continue Translation..; {0}".format(
                            #         zz))
                            time.sleep(3)
                            tryagain1()
                        except IncompleteRead as ohGodWhy:
                            # print(
                            #     "Incomplete Read Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         ohGodWhy))
                            time.sleep(3)
                            tryagain1()
                        except ValueError as ohGodWhyy:
                            # print(
                            #     "Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         ohGodWhyy))
                            time.sleep(3)
                            tryagain1()
                        except TimeoutError as stopIt:
                            # print(
                            #     "Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         stopIt))
                            time.sleep(3)
                            tryagain1()
                        except:
                            # print(
                            #     "Unknown Error error Occured, Please Make Sure You're Constantly Connected To The Internet..")
                            time.sleep(3)
                            tryagain1()

                    def tryagain():
                        try:
                            # print("Started")
                            result = r.recognize_google(audio, language=lang)
                            # language= 'ar'
                            # print('\n')
                            writeToSrt(result)
                            global aa
                            aa += 1

                        except sr.UnknownValueError:
                            # print("could not understand audio")
                            # print(1)
                            # tryagain1()
                            # print("could not understand audio.. ")
                            result = ' '
                            writeToSrt(result)
                            aa += 1
                        except sr.RequestError as e:
                            # print("could not understand audio {0}".format(e))
                            # print("trying again")
                            time.sleep(3)
                            tryagain1()
                        except ConnectionError as a:
                            # print("error; {0}".format(a))
                            # print("CONNECTION ERROR, Trying Again..")
                            time.sleep(3)
                            tryagain()
                        except RecursionError as b:
                            # print("Recursive error; {0}".format(b))
                            time.sleep(3)
                            tryagain1()
                        except ProxyError as zz:
                            # print(
                            #     "Proxy Error error Occured, Please Change Your Ip To Continue Translation..; {0}".format(
                            #         zz))
                            time.sleep(3)
                            tryagain()
                        except IncompleteRead as ohGodWhy:
                            # print(
                            #     "Incomplete Read Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         ohGodWhy))
                            time.sleep(3)
                            tryagain()
                        except ValueError as ohGodWhyy:
                            # print(
                            #     "Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         ohGodWhyy))
                            time.sleep(3)
                            tryagain()
                        except TimeoutError as stopIt:
                            # print(
                            #     "Value Error error Occured, Please Make Sure You're Constantly Connected To The Internet..; {0}".format(
                            #         stopIt))
                            time.sleep(3)
                            tryagain()
                        # except:
                        #     print(
                        #         "Unknown Error error Occured, Please Make Sure You're Constantly Connected To The Internet..")
                        #     time.sleep(3)
                        #     tryagain()

                    tryagain()
                ii += 1

            except PermissionError as rip:
                # print('This Folder Has No mp4 {0}'.format(rip))
                # print("\n")
                ii -= 1

        for fffname in os.listdir(sourceVideosFolder):
            input = sourceVideosFolder + r'\%s' % (str(fffname))
            newVideooName = fffname.replace("-s-", " ")
            newVideooNameX = newVideooName.replace("-a-", "&")
            inputNameee = sourceVideosFolder + r'\%s' % (newVideooNameX)
            os.rename(input, inputNameee)

        iii = 0
        for ffffname in os.listdir(outputSubtitlesFolder):
            videoss = os.listdir(sourceVideosFolder)
            srtts = os.listdir(outputSubtitlesFolder)
            originalSrtName = outputSubtitlesFolder + '\%s' % (srtts[iii])
            originalVideoName = videoss[iii]
            shutil.copy(originalSrtName, temporarySubtitles)
            srttss = os.listdir(temporarySubtitles)
            originalSrtName2 = temporarySubtitles + '\%s' % (srttss[0])
            newSrtName = temporarySubtitles + '\%s' % (originalVideoName[:-4]) + '.srt'
            os.rename(originalSrtName2, newSrtName)
            shutil.copy(newSrtName, FinishedSubtitles)
            os.remove(newSrtName)
            iii += 1

        copy_tree(FinishedSubtitles, sourceVideosFolder)


        def find(name, path):
            for root, dirs, files in os.walk(path):
                if name in files:
                    return os.path.join(root)  # return os.path.join(root, name)

        def getVideoExtension():
            videoSample = os.listdir(sourceVideosFolder)
            videoSample = videoSample[0]
            videoSample = videoSample[-4:]
            return videoSample

        iii = 0
        for ffffname in os.listdir(FinishedSubtitles):
            srtts = os.listdir(FinishedSubtitles)
            originalSrtName = FinishedSubtitles + '\%s' % (srtts[iii])
            name = srtts[iii]
            name = name[:-4]
            shutil.copy(originalSrtName, str(find(name + str(getVideoExtension()), whereToLookToMatchHierarchy)))
            iii += 1

        copy_tree(archiveFolder, FinishedSubtitles)

        self.label_4.setText('Finished!')
        self.progressBar.setProperty("value", 100)
        self.pushButton_4.setDisabled(False)

        # self.label_2.setText('Time')
        # self.label_3.setText('Output')

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Subtytor"))
        self.pushButton.setText(_translate("MainWindow", "file"))
        self.pushButton_2.setText(_translate("MainWindow", "folder"))
        self.label.setText(_translate("MainWindow", "Select a:"))
        self.pushButton_3.setText(_translate("MainWindow", "About"))
        self.pushButton_4.setText(_translate("MainWindow", "Start"))
        self.progressBar.setFormat(_translate("MainWindow", "%p%"))
        self.label_2.setText(_translate("MainWindow", "Time"))
        self.label_3.setText(_translate("MainWindow", "Output"))
        self.label_4.setText(_translate("MainWindow", "Status"))
        self.label_5.setText(_translate("MainWindow", "Selected"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)


    ui = Ui_MainWindow()


    sys.exit(app.exec_())

# Code Source: https://pythonprogramminglanguage.com/pyqt5-video-widget/

"""
x Add that video loads on screen when selected
x Add resume/pause button
x Add fast forward/rewind button
X Select file should also load the metadata file as well
Add smart rewind button functionality and add visual markers on progress bar
Check how to add this codec "https://www.codecguide.com/configuration_tips.htm?version=1820" as a requirement
See if its possible to convert this to .exe file
"""
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QAction, QMessageBox
from PyQt5.QtGui import QCloseEvent, QIcon
import sys

from controller import Controller
from eventlogger import Logger, ErrorLogger

class Viewer(QMainWindow):
    def __init__(self, controller: Controller, app: QApplication, logger: Logger, errorLogger: ErrorLogger):
        self.errorLogger = errorLogger
        self.logger = None
        super().__init__()
        self.setWindowTitle("Smart Rewind Media Player")
        try:
            self.__init(controller, app, logger, errorLogger)
        except Exception as e:
            self.errorLogger.log({
                "type": "EXCEPTION",
                "error": str(e)
            })
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(f'Error encountered: {e}')
            msg.setWindowTitle("Error")
            msg.exec_()
            self.closeEvent(None)
            raise Exception(e)

    def __init(self, controller: Controller, app: QApplication, logger: Logger): 
        self.controller = controller
        self.app = app
        self.logger = logger

        videoWidget = QVideoWidget()
        # self.errorLabel = QLabel()
        # self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
        #         QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        menuBar.setStyleSheet("border-top: 2px inset #e6e5e1;")
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.controller.positionSlider.getTimeViewer())
        controlLayout.addWidget(self.controller.positionSlider)

        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.controller.charSmartRewindButton)
        buttonLayout.addWidget(self.controller.sceneRewindButton)
        buttonLayout.addWidget(self.controller.backwardButton)
        buttonLayout.addWidget(self.controller.playButton)
        buttonLayout.addWidget(self.controller.forwardButton)
        buttonLayout.addWidget(self.controller.sceneForwardButton)
        buttonLayout.addWidget(self.controller.charSmartForwardButton)
        buttonLayout.addWidget(self.controller.returnToTimestampButton)
        buttonLayout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addLayout(buttonLayout)
        # layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.controller.mediaPlayer.setVideoOutput(videoWidget)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose Video",
                self.controller.getLastOpenedFolder(), "Video (*.mp4 *.avi *.mkv *.mpeg *.flv *.mov)")

        metadataFileName, _ = QFileDialog.getOpenFileName(self, "Choose Metadata File",
                self.controller.getLastOpenedFolder(), "Text (*.txt)")
        self.controller.open_file(fileName, metadataFileName)

    def exitCall(self):
        self.logger.stop()
        sys.exit(self.app.exec_())

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.logger is not None:
            self.logger.stop()
        self.errorLogger.stop()
        return super().closeEvent(a0)
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
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys
from PyQt5.QtCore import QSettings

from buttons import PlayButton, ForwardButton, BackwardButton, CharacterSmartRewindButton, SceneSmartRewindButton, SceneSmartForwardButton, CharacterSmartForwardButton, ReturnToLastTimestampButton
from model import Model
from slider import Slider

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Smart Rewind ") 
        self.model = Model()
        self.settings = QSettings("pyqt_settings.ini", QSettings.IniFormat)
        self.lastFolderOpened = self.settings.value("LastFolder")
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.positionSlider = Slider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        videoWidget = QVideoWidget()

        self.playButton = PlayButton(self.mediaPlayer)
        self.forwardButton = ForwardButton(self.mediaPlayer)
        self.backwardButton = BackwardButton(self.mediaPlayer)
        self.charSmartRewindButton = CharacterSmartRewindButton(self.mediaPlayer, self.positionSlider)
        self.sceneRewindButton = SceneSmartRewindButton(self.mediaPlayer, self.positionSlider)
        self.charSmartForwardButton = CharacterSmartForwardButton(self.mediaPlayer, self.positionSlider)
        self.sceneForwardButton = SceneSmartForwardButton(self.mediaPlayer, self.positionSlider)
        self.returnToTimestampButton = ReturnToLastTimestampButton(self.mediaPlayer, self.positionSlider)

        self.timeViewer = QLabel()
        self.timeViewer.setText(self.model.getTimeLabelStr())

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

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
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.timeViewer)
        controlLayout.addWidget(self.positionSlider)

        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.charSmartRewindButton)
        buttonLayout.addWidget(self.sceneRewindButton)
        buttonLayout.addWidget(self.backwardButton)
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.forwardButton)
        buttonLayout.addWidget(self.sceneForwardButton)
        buttonLayout.addWidget(self.charSmartForwardButton)
        buttonLayout.addWidget(self.returnToTimestampButton)
        buttonLayout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self):
        if self.lastFolderOpened == "":
            self.lastFolderOpened = QDir.currentPath()

        fileName, _ = QFileDialog.getOpenFileName(self, "Choose Video",
                self.lastFolderOpened, "Video (*.mp4 *.avi *.mkv *.mpeg *.flv *.mov)")
        self.lastFolderOpened = "/".join(fileName.split("/")[:-1])

        metadataFileName, _ = QFileDialog.getOpenFileName(self, "Choose Metadata File",
                self.lastFolderOpened, "Text (*.txt)")
        self.lastFolderOpened = "/".join(metadataFileName.split("/")[:-1])

        self.settings.setValue("LastFolder", self.lastFolderOpened)

        if metadataFileName != '':
            with open(metadataFileName, "r") as f:
                self.model.setTimeslots(eval(f.read()))

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
            self.backwardButton.setEnabled(True)
            self.charSmartForwardButton.setup(self.model)
            self.charSmartRewindButton.setup(self.model)
            self.sceneRewindButton.setup(self.model)
            self.sceneForwardButton.setup(self.model)
            self.returnToTimestampButton.setup(self.model)
            self.play()

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.model.setCurrentDuration(position)
        self.timeViewer.setText(self.model.getTimeLabelStr())

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        self.model.setTotalDuration(duration)
        self.model.setCurrentDuration(0)
        self.timeViewer.setText(self.model.getTimeLabelStr())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        self.model.setCurrentDuration(position)
        self.timeViewer.setText(self.model.getTimeLabelStr())

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
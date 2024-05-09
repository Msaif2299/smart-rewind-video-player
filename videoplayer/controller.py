from model import Model
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent

from buttons import PlayButton, ForwardButton, BackwardButton, CharacterSmartRewindButton, SceneSmartRewindButton, SceneSmartForwardButton, CharacterSmartForwardButton, ReturnToLastTimestampButton
from slider import Slider
from mediaplayer import MediaPlayer
from eventlogger import Logger
import os
import pysrt

class Controller:
    def __init__(self, model: Model, logger: Logger) -> None:
        self.mediaPlayer = MediaPlayer()
        self.positionSlider = Slider()
        self.model = model

        self.playButton = PlayButton(self.mediaPlayer, logger)
        self.forwardButton = ForwardButton(self.mediaPlayer, logger)
        self.backwardButton = BackwardButton(self.mediaPlayer, logger)
        self.charSmartRewindButton = CharacterSmartRewindButton(self.mediaPlayer, self.positionSlider, logger)
        self.sceneRewindButton = SceneSmartRewindButton(self.mediaPlayer, self.positionSlider, logger)
        self.charSmartForwardButton = CharacterSmartForwardButton(self.mediaPlayer, self.positionSlider, logger)
        self.sceneForwardButton = SceneSmartForwardButton(self.mediaPlayer, self.positionSlider, logger)
        self.returnToTimestampButton = ReturnToLastTimestampButton(self.mediaPlayer, self.positionSlider, logger)

        self.mediaPlayer.setup(self.model, self.positionSlider, self.playButton)
        self.positionSlider.setup(self.model, self.mediaPlayer)

    def getLastOpenedFolder(self) -> str:
        if self.model.getLastOpenedFolder() == "" or self.model.getLastOpenedFolder() is None:
            self.model.setLastOpenedFolder(QDir.currentPath())
        return self.model.getLastOpenedFolder()

    def open_file(self, fileName, metadataFileName):
        self.model.setLastOpenedFolder("/".join(metadataFileName.split("/")[:-1]))

        if metadataFileName == '':
            return
        with open(metadataFileName, "r") as f:
            self.model.setTimeslots(eval(f.read()))

        if fileName == '':
            return
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
        self.playButton.playorpause()
        subtitleFile = fileName.split(".")[0] + ".srt"
        if not os.path.exists(subtitleFile):
            return
        self.model.setSubtitles(pysrt.open(subtitleFile))
            

        
from model import Model
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtMultimedia import QMediaContent

from buttons import PlayButton, ForwardButton, BackwardButton, CharacterSmartRewindButton, SceneSmartRewindButton, SceneSmartForwardButton, CharacterSmartForwardButton, ReturnToLastTimestampButton
from slider import Slider
from mediaplayer import MediaPlayer
from eventlogger import Logger
from checkbox import SubtitleCheckBox
from labels import AlertLabel
from cardpanels import CharSmartForwardPanel, CharSmartRewindPanel
import os
import pysrt

class Controller:
    def __init__(self, model: Model, logger: Logger) -> None:
        self.mediaPlayer = MediaPlayer()
        self.positionSlider = Slider()
        self.model = model
        self.logger = logger

        self.alertLabel = AlertLabel(self.model)
        self.playButton = PlayButton(self.mediaPlayer, self.logger, self.model)
        self.forwardButton = ForwardButton(self.mediaPlayer, self.logger, self.model)
        self.backwardButton = BackwardButton(self.mediaPlayer, self.logger, self.model)
        # self.charSmartRewindButton = CharacterSmartRewindButton(self.mediaPlayer, self.positionSlider, self.logger, self.model)
        self.sceneRewindButton = SceneSmartRewindButton(self.mediaPlayer, self.positionSlider, self.logger, self.model)
        # self.charSmartForwardButton = CharacterSmartForwardButton(self.mediaPlayer, self.positionSlider, self.logger, self.model)
        self.sceneForwardButton = SceneSmartForwardButton(self.mediaPlayer, self.positionSlider, self.logger, self.model)
        self.returnToTimestampButton = ReturnToLastTimestampButton(self.mediaPlayer, self.positionSlider, self.logger, self.model)
        self.subtitlesEnabledCheckBox = SubtitleCheckBox(self.model, self.logger)

        self.setupSidePanels()

        self.mediaPlayer.setup(self.model, self.positionSlider, self.playButton)
        self.positionSlider.setup(self.model, self.mediaPlayer)

    def setupSidePanels(self):
        self.charSmartForwardPanel = CharSmartForwardPanel(self.mediaPlayer,self.positionSlider, self.model,  self.logger)
        self.charSmartRewindPanel = CharSmartRewindPanel(self.mediaPlayer, self.positionSlider, self.model, self.logger)

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
        self.model.reset()
        self.positionSlider.hideTicker()
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent())
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
        self.playButton.setEnabled(True)
        self.forwardButton.setEnabled(True)
        self.backwardButton.setEnabled(True)
        self.sceneRewindButton.setup(self.model)
        self.sceneForwardButton.setup(self.model)
        self.returnToTimestampButton.setup(self.model)
        self.playButton.playorpause()
        charImageFolder = self.getLastOpenedFolder() + "/character_images"
        self.charSmartForwardPanel.populateCharacters(charImageFolder)
        self.charSmartRewindPanel.populateCharacters(charImageFolder)
        subtitleFile = fileName.split(".")[0] + ".srt"
        if not os.path.exists(subtitleFile):
            return
        self.model.setSubtitles(pysrt.open(subtitleFile))
        self.subtitlesEnabledCheckBox.enableCheckBox()
            

        
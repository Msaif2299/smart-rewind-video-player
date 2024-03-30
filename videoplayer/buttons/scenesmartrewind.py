from .base import Button
from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
import os

class SceneSmartRewindButton(Button):
    def __init__(self, mediaPlayer, positionSlider) -> None:
        icon = QtGui.QIcon(QFileInfo(__file__).absolutePath() + '/../assets/scenesmartrewindicon.ico')
        super().__init__(icon, mediaPlayer, positionSlider, self.smartRewind)

    def setup(self, model):
        self.model = model
        self.scene_slots = self.model.getSceneTimeslots()
        self.setEnabled(True)

    def smartRewind(self):
        cur_time = self.model.getCurrentDuration()
        for slot in reversed(self.scene_slots):
            if slot[1] >= cur_time:
                continue
            if not self.slider.isTickerVisible():
                self.slider.showTicker()
                self.slider.setTickerPosition(cur_time)
                self.model.setStoredDuration(cur_time)
            self.mediaPlayer.setPosition(slot[0])
            return
        self.alert(self.model.isWindows)
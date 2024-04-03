from .base import Button
from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo

class SceneSmartForwardButton(Button):
    def __init__(self, mediaPlayer, positionSlider, logger) -> None:
        icon = QtGui.QIcon(QFileInfo(__file__).absolutePath() + '/../assets/scenesmartforwardicon.ico')
        super().__init__(icon, mediaPlayer, positionSlider, self.smartForward, logger)

    def setup(self, model):
        self.model = model
        self.scene_slots = self.model.getSceneTimeslots()
        self.setEnabled(True)

    def smartForward(self):
        cur_time = self.model.getCurrentDuration()
        for slot in self.scene_slots:
            if slot[0] <= cur_time:
                continue
            if not self.slider.isTickerVisible():
                self.slider.showTicker()
                self.slider.setTickerPosition(cur_time)
                self.model.setStoredDuration(cur_time)
            self.log_data(True, slot[0])
            self.mediaPlayer.setPosition(slot[0])
            return
        self.alert(self.model.isWindows)
        self.log_data(False, -1)

    def log_data(self, success: bool, new_timestamp: int) -> str:
        data = {
            "e_name": "SceneSmartForwardButtonPressed",
            "current_timestamp": self.mediaPlayer.position(),
            "new_timestamp": new_timestamp,
            "success": success
        }
        self.logger.log(data)
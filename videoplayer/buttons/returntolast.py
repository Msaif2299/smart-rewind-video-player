from .base import Button
from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
from .common import resource_path

class ReturnToLastTimestampButton(Button):
    def __init__(self, mediaPlayer, positionSlider, logger) -> None:
        icon = QtGui.QIcon(resource_path('returntotimestampicon.ico'))
        super().__init__(icon, mediaPlayer, positionSlider, self._return, logger)

    def setup(self, model):
        self.model = model
        self.setEnabled(True)

    def _return(self):
        if not self.slider.isTickerVisible() or self.model.getStoredDuration() == 0:
            self.alert(self.model.isWindows)
            self.log_data(False, -1)
            return
        self.slider.hideTicker()
        self.log_data(True, self.model.getStoredDuration())
        self.mediaPlayer.setPosition(self.model.getStoredDuration())

    def log_data(self, success: bool, new_timestamp: int) -> str:
        data = {
            "e_name": "ReturnToLastTimestampButtonPressed",
            "current_timestamp": self.mediaPlayer.position(),
            "success": success,
            "new_timestamp": new_timestamp
        }
        self.logger.log(data)
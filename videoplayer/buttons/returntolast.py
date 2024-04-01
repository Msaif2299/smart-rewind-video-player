from .base import Button
from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo

class ReturnToLastTimestampButton(Button):
    def __init__(self, mediaPlayer, positionSlider, logger) -> None:
        icon = QtGui.QIcon(QFileInfo(__file__).absolutePath() + '/../assets/returntotimestampicon.ico')
        super().__init__(icon, mediaPlayer, positionSlider, self._return, logger)

    def setup(self, model):
        self.model = model
        self.setEnabled(True)

    def _return(self):
        if not self.slider.isTickerVisible() or self.model.getStoredDuration() == 0:
            self.alert(self.model.isWindows)
            return
        self.slider.hideTicker()
        self.mediaPlayer.setPosition(self.model.getStoredDuration())
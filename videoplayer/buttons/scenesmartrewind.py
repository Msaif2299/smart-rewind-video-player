from .base import Button
from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
import os

class SceneSmartRewindButton(Button):
    def __init__(self, mediaPlayer, model) -> None:
        icon = QtGui.QIcon(QFileInfo(__file__).absolutePath() + '/../assets/scenesmartrewindicon.ico')
        super().__init__(icon, mediaPlayer, self.smartRewind)
        self.model = model

    def smartRewind(self):
        pass
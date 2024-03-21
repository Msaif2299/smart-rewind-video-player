from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QStyle
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from .base import Button

class BackwardButton(Button):
    def __init__(self, mediaPlayer) -> None:
        super().__init__(QStyle.SP_MediaSkipBackward, mediaPlayer, self.backward)

    def backward(self):
        if self.mediaPlayer.position() - 10000 < 0:
            self.mediaPlayer.setPosition(0)
            return
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000)
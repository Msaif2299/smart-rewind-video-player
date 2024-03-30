from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QStyle
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from .base import Button

class ForwardButton(Button):
    def __init__(self, mediaPlayer) -> None:
        super().__init__(QStyle.SP_MediaSkipForward, mediaPlayer, None, self.forward)

    def forward(self):
        if self.mediaPlayer.duration() < self.mediaPlayer.position() + 10000:
            self.mediaPlayer.setPosition(self.mediaPlayer.duration())
            return
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)
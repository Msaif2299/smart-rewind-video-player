from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QStyle
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from .base import Button

class PlayButton(Button):
    def __init__(self, mediaPlayer) -> None:
        super().__init__(QStyle.SP_MediaPlay, mediaPlayer, self.play)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.mediaPlayer.pause()
        else:
            self.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.mediaPlayer.play()
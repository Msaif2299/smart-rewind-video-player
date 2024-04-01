from __future__ import annotations
from typing import TYPE_CHECKING
from PyQt5.QtWidgets import QStyle
from PyQt5.QtMultimedia import QMediaPlayer
from .base import Button
if TYPE_CHECKING:
    from videoplayer.mediaplayer import MediaPlayer

class PlayButton(Button):
    def __init__(self, mediaPlayer: MediaPlayer, logger) -> None:
        super().__init__(QStyle.SP_MediaPlay, mediaPlayer, None, self.playorpause, logger)

    def changeIcon(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            return
        self.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def playorpause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            return
        self.mediaPlayer.play()
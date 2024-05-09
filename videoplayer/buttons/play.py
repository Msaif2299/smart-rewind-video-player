from __future__ import annotations
from typing import TYPE_CHECKING
from PyQt5.QtWidgets import QStyle
from PyQt5.QtMultimedia import QMediaPlayer
from .base import Button
if TYPE_CHECKING:
    from videoplayer.mediaplayer import MediaPlayer
    from videoplayer.model import Model

class PlayButton(Button):
    def __init__(self, mediaPlayer: MediaPlayer, logger, model: Model) -> None:
        super().__init__(QStyle.SP_MediaPlay, mediaPlayer, None, self.playorpause, logger, model)
        self.setToolTip("Press to Play or Pause the video")

    def changeIcon(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            return
        self.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def playorpause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.pause_log_data()
            return
        self.mediaPlayer.play()
        self.play_log_data()

    def play_log_data(self) -> str:
        data = {
            "e_name": "PlayButtonPressed",
            "current_timestamp": self.mediaPlayer.position()
        }
        self.logger.log(data)

    def pause_log_data(self) -> str:
        data = {
            "e_name": "PauseButtonPressed",
            "current_timestamp": self.mediaPlayer.position(),
        }
        self.logger.log(data)

    
from PyQt5.QtWidgets import QStyle
from .base import Button

FORWARD_IN_MS = 10000

class ForwardButton(Button):
    def __init__(self, mediaPlayer, logger) -> None:
        super().__init__(QStyle.SP_MediaSkipForward, mediaPlayer, None, self.forward, logger)

    def forward(self):
        if self.mediaPlayer.duration() < self.mediaPlayer.position() + FORWARD_IN_MS:
            self.log_data(self.mediaPlayer.duration())
            self.mediaPlayer.setPosition(self.mediaPlayer.duration())
            return
        self.log_data(self.mediaPlayer.position() + FORWARD_IN_MS)
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + FORWARD_IN_MS)

    def log_data(self, new_timestamp) -> str:
        data = {
            "e_name": "ForwardButtonPressed",
            "current_timestamp": self.mediaPlayer.position(),
            "new_timestamp": new_timestamp
        }
        self.logger.log(data)
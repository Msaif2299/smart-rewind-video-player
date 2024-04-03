from PyQt5.QtWidgets import QStyle
from .base import Button
from eventlogger import Logger

BACKWARD_IN_MS = 10000

class BackwardButton(Button):
    def __init__(self, mediaPlayer, logger: Logger) -> None:
        super().__init__(QStyle.SP_MediaSkipBackward, mediaPlayer, None, self.backward, logger)

    def backward(self):
        if self.mediaPlayer.position() - BACKWARD_IN_MS < 0:
            self.mediaPlayer.setPosition(0)
            self.log_data(0)
            return
        self.log_data(self.mediaPlayer.position() - BACKWARD_IN_MS)
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - BACKWARD_IN_MS)

    def log_data(self, new_timestamp) -> str:
        data = {
            "e_name": "BackwardButtonPressed",
            "current_timestamp": self.mediaPlayer.position(),
            "new_timestamp": new_timestamp
        }
        self.logger.log(data)

from PyQt5.QtWidgets import QStyle
from .base import Button

class ForwardButton(Button):
    def __init__(self, mediaPlayer, logger) -> None:
        super().__init__(QStyle.SP_MediaSkipForward, mediaPlayer, None, self.forward, logger)

    def forward(self):
        if self.mediaPlayer.duration() < self.mediaPlayer.position() + 10000:
            self.mediaPlayer.setPosition(self.mediaPlayer.duration())
            return
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)
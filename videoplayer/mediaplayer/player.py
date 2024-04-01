from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimedia import QMediaPlayer
if TYPE_CHECKING:
    from videoplayer.slider import Slider
    from videoplayer.model import Model
    from videoplayer.buttons import PlayButton

class MediaPlayer(QMediaPlayer):
    def __init__(self) -> None:
        super().__init__(None, QMediaPlayer.VideoSurface)

    def setup(self, model: Model, slider: Slider, playbutton: PlayButton):
        self.model = model
        self.slider = slider
        self.playbutton = playbutton
        self.stateChanged.connect(self._mediaStateChanged)
        self.positionChanged.connect(self._positionChanged)
        self.durationChanged.connect(self._durationChanged)
        self.error.connect(self._handleError)

    def _mediaStateChanged(self, state):
        self.playbutton.changeIcon()

    def _positionChanged(self, position):
        self.slider.setValue(position)

    def _durationChanged(self, duration):
        self.slider.setRange(0, duration)
        self.model.setTotalDuration(duration)
        self.slider.setValue(0)

    def _handleError(self):
        self.playbutton.setEnabled(False)
        print("Error: " + self.errorString())
        #self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt5.QtGui import QPaintEvent, QPainter, QColor, QPainterPath
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSlider

if TYPE_CHECKING:
    from videoplayer.model import Model
    from videoplayer.mediaplayer import MediaPlayer

class Slider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.shouldShowTicker = False
        self.tickerPosition = 0
        self.timeviewer = QLabel()

    def setup(self, model: Model, media_player: MediaPlayer):
        self.model = model
        self.media_player = media_player
        self.setRange(0, 0)
        self.sliderMoved.connect(self.setPosition)
        self.timeviewer.setText(self.model.getTimeLabelStr())

    def setValue(self, position):
        super().setValue(position)
        self.model.setCurrentDuration(position)
        self.timeviewer.setText(self.model.getTimeLabelStr())

    def setTickerPosition(self, position: int):
        self.tickerPosition = position

    def isTickerVisible(self) -> bool:
        return self.shouldShowTicker

    def showTicker(self):
        self.shouldShowTicker = True

    def hideTicker(self):
        self.shouldShowTicker = False
    
    def paintEvent(self, ev: QPaintEvent | None) -> None:
        super().paintEvent(ev)
        if not self.shouldShowTicker:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        painter.setPen(QColor('green'))
        x_div = float(self.width()/self.maximum())
        path.addRect(QRectF(int(x_div*self.tickerPosition), 2, 6, 4))
        painter.fillPath(path, QColor('green'))
        painter.setPen(QColor('green'))
        x_coord = int(x_div*(self.tickerPosition)+3)
        painter.drawLine(x_coord, 16, x_coord, 2)

    def setPosition(self, position):
        self.media_player.setPosition(position)
        self.model.setCurrentDuration(position)
        self.timeviewer.setText(self.model.getTimeLabelStr())

    def getTimeViewer(self):
        return self.timeviewer


from PyQt5.QtGui import QPaintEvent, QPainter, QColor, QPainterPath
from PyQt5.QtWidgets import QSlider, QWidget
from typing import Optional
from PyQt5.QtCore import QRectF

class Slider(QSlider):
    def __init__(self, parent: Optional[QWidget] = ...):
        super().__init__(parent)
        self.shouldShowTicker = False
        self.tickerPosition = 0

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


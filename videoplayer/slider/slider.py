from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt5.QtGui import QMouseEvent, QPaintEvent, QPainter, QColor, QPainterPath, QPaintDevice
from PyQt5.QtWidgets import QSlider, QStyle, QStyleOption, QWidget, QRadioButton, QHBoxLayout, QVBoxLayout, QBoxLayout, QStyle, QProxyStyle
from PyQt5.QtCore import QRectF, Qt, QPoint, QRect, QPointF
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSlider

if TYPE_CHECKING:
    from videoplayer.model import Model
    from videoplayer.mediaplayer import MediaPlayer

"""
Slider size handling: https://stackoverflow.com/questions/62916755/qslider-handle-size-pyqt5
Slider round: https://forum.qt.io/topic/87256/how-to-set-qslider-handle-to-round/2
"""

class TimestampClickableObject:
    """
    For each character scene, a clickable object on the slider
    ...

    Attributes
    ----------
    rect : QRectF
        Lower rectangle in display, imported from PyQt5.QtCore
    line : tuple[QPointF,QPointF]
        Line defined by (x1, x2, y1, y2)
    """
    rect: QRectF
    line: tuple[QPointF,QPointF]
    parent: QPaintDevice|None
    timestamp: int
    pressed: bool

    def __init__(self, rect: QRectF, line: tuple[QPointF,QPointF], widget: QPaintDevice|None, timestamp: int) -> None:
        self.rect = rect
        self.line = line
        self.widget = widget
        self.timestamp = timestamp
        self.pressed = False

    def draw(self):
        painter = QPainter(self.widget)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRect(self.rect)
        fillColor = QColor('green')
        if self.pressed:
            fillColor = QColor('red')
        painter.fillPath(path, fillColor)
        painter.setPen(fillColor)
        painter.drawLine(*self.line)

class SliderHandleProxy(QProxyStyle):
    def pixelMetric(self, metric: QStyle.PixelMetric, option: QStyleOption | None = ..., widget: QWidget | None = ...) -> int:
        if metric == QStyle.PM_SliderThickness:
            return 40
        elif metric == QStyle.PM_SliderLength:
            return 40
        return super().pixelMetric(metric, option, widget)

class Slider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.shouldShowTicker = False
        self.tickerPosition = 0
        self.timeviewer = QLabel()
        self.timestampRects: list[TimestampClickableObject] = [] # to jump to the timestamp shown by marker for char scenes
        self.setFixedHeight(75)
        self.setStyle(SliderHandleProxy(self.style()))
        self.setStyleSheet("""
        QSlider::groove:horizontal { 
            background-color: grey;
            border: 0px solid #424242; 
            height: 10px; 
            border-radius: 4px;
        }

        QSlider::handle:horizontal { 
            background-color: #5c94ed; 
            border: 2px solid #064ab8; 
            width: 16px; 
            height: 20px; 
            line-height: 20px; 
            margin-top: -5px; 
            margin-bottom: -5px; 
            border-radius: 10px; 
        }

        QSlider::handle:horizontal:hover { 
            border-radius: 10px;
        }
        QSlider::add-page:horizontal {
            background: grey;
        }
        QSlider::sub-page:horizontal {
            background: #5c94ed;
        }
        """)

    def setup(self, model: Model, media_player: MediaPlayer):
        self.model = model
        self.media_player = media_player
        self.setRange(0, 0)
        self.sliderMoved.connect(self.setPosition)
        self.timeviewer.setText(self.model.getTimeLabelStr())
        self.model.populateTimestampSignal.connect(self.populateTimestampRects)
    
    def mousePressEvent(self, ev: QMouseEvent | None) -> None:
        for marker in self.timestampRects:
            if marker.rect.contains(ev.pos().x(), ev.pos().y()):
                if not self.isTickerVisible():
                    self.model.setStoredDuration(self.model.getCurrentDuration())
                    self.setTickerPosition(self.model.getCurrentDuration())
                    self.showTicker()
                self.setPosition(marker.timestamp[0])
                marker.pressed = True
                self.update()
                break
        super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent | None) -> None:
        for marker in self.timestampRects:
            marker.pressed = False
        self.update()
        return super().mouseReleaseEvent(ev)

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

    def populateTimestampRects(self):
        self.timestampRects = []
        timeslots = self.model.getCharTimeslots()[self.model.currentChosenCharacter]
        for timeslot in timeslots:
            x_div = float(self.width()/self.maximum())
            rect = QRectF(int(x_div*timeslot[0])-6, 0, 36, 36)
            x_coord = x_div*(timeslot[0])
            # should look into this more, might want to create a fully custom QSlider from scratch that has all the slider and handle props available
            line = (QPointF(x_coord, 16), QPointF(x_coord, 2))
            rect = TimestampClickableObject(
                rect,
                line,
                self,
                timeslot
            )
            self.timestampRects.append(rect)


    def drawStoredTimestampMarker(self):
        if not self.shouldShowTicker:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        painter.setPen(QColor('green'))
        x_div = float(self.width()/self.maximum())
        path.addRect(QRectF(int(x_div*self.tickerPosition), 20, 6, 4))
        painter.fillPath(path, QColor('green'))
        painter.setPen(QColor('green'))
        x_coord = x_div*(self.tickerPosition)+3
        painter.drawLine(QPointF(x_coord, 46), QPointF(x_coord, 20))

    def drawLastSetCharacterTimestamps(self):
        if self.model is None:
            return
        if self.model.currentChosenCharacter == "":
            return
        for timestampObj in self.timestampRects:
            timestampObj.draw()
    
    def paintEvent(self, ev: QPaintEvent | None) -> None:
        self.drawStoredTimestampMarker()
        self.drawLastSetCharacterTimestamps()
        super().paintEvent(ev)

    def setPosition(self, position):
        self.media_player.setPosition(position)
        self.model.setCurrentDuration(position)
        self.timeviewer.setText(self.model.getTimeLabelStr())

    def getTimeViewer(self):
        return self.timeviewer


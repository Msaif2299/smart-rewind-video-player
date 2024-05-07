"""
Stylesheet source: https://forum.qt.io/topic/41771/solved-setstylesheet-to-qpushbutton-rounded-corners/12
"""

from PyQt5.QtWidgets import QPushButton, QStyle
from PyQt5.QtCore import QTimer
import winsound
import sys
from typing import Optional
from slider import Slider
from mediaplayer import MediaPlayer
from eventlogger import Logger

class Button(QPushButton):
    def __init__(self, icon, mediaPlayer: MediaPlayer, positionSlider: Optional[Slider], action, logger: Logger) -> None:
        super().__init__()
        self.setEnabled(False)
        self.setStyleSheet("""
            QPushButton {
                color: #333;
                border: 2px solid #555;
                border-radius: 20px;
                border-style: outset;
                background: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #888
                );
                padding: 5px;
            }
                           
            QPushButton::menu-indicator {
                width: 0px;
            }

            QPushButton:hover {
                background: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #bbb
                );
            }

            QPushButton:pressed {
                border-style: inset;
                background: qradialgradient(
                    cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,
                    radius: 1.35, stop: 0 #fff, stop: 1 #ddd
                );
            }"""
        )
        if type(icon) is QStyle.StandardPixmap:
            self.setIcon(self.style().standardIcon(icon))
        else:
            self.setIcon(icon)
        if action is not None:
            self.clicked.connect(action)
        self.mediaPlayer = mediaPlayer
        self.slider = positionSlider
        self.logger = logger

    def alert(self, isWindows):
        if isWindows:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) 
            return  
        sys.stdout.write('\a')
        sys.stdout.flush()

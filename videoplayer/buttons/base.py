"""
Stylesheet source: https://forum.qt.io/topic/41771/solved-setstylesheet-to-qpushbutton-rounded-corners/12
"""

from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QStyle
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

class Button(QPushButton):
    def __init__(self, icon, mediaPlayer, action) -> None:
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
        self.clicked.connect(action)
        self.mediaPlayer = mediaPlayer

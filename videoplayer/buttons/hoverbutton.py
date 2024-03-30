import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMenu, QAction
from .base import Button
from typing import List

class HoverButtonAction:
    def __init__(self, display_name, action):
        self.name = display_name
        self.action = action

class HoverButton(Button):
    def __init__(self, icon, mediaPlayer, positionSlider):
        super().__init__(icon, mediaPlayer, positionSlider, None)
        self.setMouseTracking(True)
        self.menu = QMenu(self)
    
    def setOptions(self, actions: List[HoverButtonAction]):
        for action in actions:
            qaction = QAction(action.name, self)
            qaction.triggered.connect(action.action)
            self.menu.addAction(qaction)

    def enterEvent(self, event):
        self.menu.exec_(self.mapToGlobal(self.rect().bottomLeft()))

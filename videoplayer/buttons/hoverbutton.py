from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from videoplayer.model import Model
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import QEvent
from .base import Button
from typing import List

class HoverButtonAction:
    def __init__(self, display_name, action, tooltip):
        self.name = display_name
        self.action = action
        self.tooltip = tooltip

class HoverButton(Button):
    def __init__(self, icon, mediaPlayer, positionSlider, logger, model):
        super().__init__(icon, mediaPlayer, positionSlider, None, logger, model)
        self.setMouseTracking(True)
        self.menu = QMenu(self)
        self.setMenu(self.menu)
        self.menu.setToolTipsVisible(True)
    
    def setOptions(self, actions: List[HoverButtonAction]):
        self.menu.clear()
        for action in actions:
            qaction = QAction(action.name, self)
            qaction.triggered.connect(action.action)
            qaction.setToolTip(action.tooltip)
            self.menu.addAction(qaction)
        self.setMenu(self.menu)

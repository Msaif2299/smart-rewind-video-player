from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
if TYPE_CHECKING:
    from model import Model
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from typing import Callable, Tuple

class ClickableLabel(QFrame):
    baseStyle = QFrame.Panel
    """
    A label with custom action on click and stylesheet change on selected/unselected
    ...

    Attributes
    ----------
    charName : str
        Character name used for this label to show image
    isForwardLabel : bool
        Part of forward or backward labels
    action: Callable
        Custom action at Mouse Press
    model: Model
        Singleton for controlling the app
    frameDimensions: Tuple[int,int]
        Frame height and width
    """
    def __init__(self, charName: str, isForwardLabel: bool, action: Callable, model: Model, frameDimensions: Tuple[int,int], imgURL: str, text: str, imgDimensions: Tuple[int,int]):
        super().__init__()
        self.model = model
        self.action = action
        self.charName = charName
        self.isForwardLabel = isForwardLabel
        self.isSelected = False

        self.imgLabel = QLabel()
        img = QPixmap(imgURL)
        img = img.scaledToHeight(imgDimensions[0])
        img = img.scaledToWidth(imgDimensions[1])
        self.imgLabel.setPixmap(img)

        self.textLabel = QLabel(text=text)
        self.textLabel.setAlignment(Qt.AlignCenter)

        self.setFrameStyle(self.baseStyle|QFrame.Raised)
        self.setFixedHeight(frameDimensions[0])
        self.setFixedWidth(frameDimensions[1])
        self.setLineWidth(5)

        layout = QVBoxLayout()
        layout.addWidget(self.imgLabel)
        layout.addWidget(self.textLabel)
        self.setLayout(layout)

    def mousePressEvent(self, ev: QMouseEvent | None) -> None:
        self.action()
        return super().mousePressEvent(ev)
    
    def updateSelectionState(self):
        if self.model.currentChosenCharacter == self.charName and self.model.isForwardPanelClicked == self.isForwardLabel:
            self.isSelected = True
            self.setFrameStyle(self.baseStyle|QFrame.Sunken)
            self.setStyleSheet("background-color: #CBC3E3")
            return self.update()
        self.isSelected = False
        self.setFrameStyle(self.baseStyle|QFrame.Raised)
        self.setStyleSheet("background-color: none")
        self.update()

    
    
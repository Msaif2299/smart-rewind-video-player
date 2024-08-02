from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
if TYPE_CHECKING:
    from mediaplayer import MediaPlayer
    from model import Model
    from eventlogger import Logger
    from slider import Slider
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QMouseEvent, QFont
from dataclasses import dataclass
from abc import abstractmethod
import winsound
import sys
from labels import ClickableLabel

@dataclass
class PanelCard:
    name: str
    timestamps: List[List[int, int]]
    imageURL: str
    view: ClickableLabel|None

class ClickablePanel(QWidget):
    acceptedFileExtensions = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG"]
    def __init__(self, mediaPlayer: MediaPlayer, slider: Slider, model: Model, logger: Logger) -> None:
        super().__init__()
        self.mediaPlayer = mediaPlayer
        self.model = model
        self.logger = logger
        self.slider = slider

    def _createTitleLabel(self) -> QLabel:
        titleLabel = QLabel(self.title())
        titleLabel.setAlignment(Qt.AlignCenter)
        font = QFont('Arial', 10)
        font.setBold(True)
        titleLabel.setFont(font)
        return titleLabel
    
    def _createScrollableArea(self) -> QScrollArea:
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFixedWidth(175)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        return scrollArea

    def populateCharacters(self, imgFolder: str):
        self.cards: List[PanelCard] = []
        layout = QVBoxLayout()
        self.setFixedWidth(200)
        for card in self._generateCards(imgFolder):
            if card is None:
                continue
            cardView = ClickableLabel(
                card.name, 
                self.isForwardPanel(), 
                self.imageClickAction(card.name, card.timestamps), 
                self.model, 
                (150, 120),
                card.imageURL,
                card.name.title(),
                (100,100)
            )
            layout.addWidget(cardView)
            card.view = cardView
            self.cards.append(card)
        layout.addStretch()
        holderWidget = QWidget()
        holderWidget.setLayout(layout)
        holderWidget.setFixedWidth(200)
        scrollableArea = self._createScrollableArea()
        scrollableArea.setWidget(holderWidget)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._createTitleLabel())
        mainLayout.addWidget(scrollableArea, alignment=Qt.AlignHCenter)
        self.setLayout(mainLayout)

    def _generateCards(self, imgFolder: str) -> List[PanelCard]:
        if not os.path.isdir(imgFolder):
            raise Exception("Image folder not found for forward panels")
        charList = self.model.getCharTimeslots()
        if len(charList) == 0 or charList == None:
            return []
        cards = []
        for char, timeSlots in charList.items():
            cards.append(PanelCard(
                char,
                timeSlots,
                self._findImage(imgFolder, char),
                None
            ))
        return cards
    
    def _findImage(self, imgFolder, charName) -> str:
        imgFileURL = f"{imgFolder}/{charName}."
        for extension in self.acceptedFileExtensions:
            if os.path.exists(imgFileURL + extension):
                imgFileURL = imgFileURL + extension
                return imgFileURL
        raise Exception(f'Image not found for character or no acceptable image extension found (acceptable extensions include {", ".join(self.acceptedFileExtensions)})')
    
    def alert(self, isWindows: bool, message: str):
        self.model.alertSignal.emit(message)
        if isWindows:
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION) 
            return  
        sys.stdout.write('\a')
        sys.stdout.flush()
    
    @abstractmethod
    def imageClickAction(self, charName: str, timeslots: List[List[int]]) -> Callable[[None], None]:
        ...

    @abstractmethod
    def isForwardPanel(self) -> bool:
        ...

    @abstractmethod
    def title(self) -> str:
        ...

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        super().mousePressEvent(a0)
        self.updateCardsStates()

    def updateCardsStates(self):
        for card in self.cards:
            card.view.updateSelectionState()

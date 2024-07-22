from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
from videoplayer.eventlogger import Logger
from videoplayer.mediaplayer import MediaPlayer
from videoplayer.model import Model
from videoplayer.slider import Slider
if TYPE_CHECKING:
    from mediaplayer import MediaPlayer
    from model import Model
    from eventlogger import Logger
    from slider import Slider
    from PyQt5.QtGui import QMouseEvent
from .baseclickablepanel import ClickablePanel

class CharSmartForwardPanel(ClickablePanel):
    def __init__(self, mediaPlayer: MediaPlayer, slider: Slider, model: Model, logger: Logger) -> None:
        super().__init__(mediaPlayer, slider, model, logger)
        self.model.updateForwardCardsSignal.connect(self.updateCardsStates)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        super().mousePressEvent(a0)
        self.model.updateRewindCardsSignal.emit()
    
    def isForwardPanel(self) -> bool:
        return True

    def imageClickAction(self, charName: str, timeslots: List[List[int]]) -> Callable[[None], None]:
        def forward():
            self.model.setCurrentChosenCharacter(charName)
            self.model.setIsForwardPanelClicked(True)
            self.model.populateTimestampSignal.emit()
            cur_time = self.model.getCurrentDuration()
            for slot in timeslots:
                if slot[0] <= cur_time:
                    continue
                if not self.slider.isTickerVisible():
                    self.slider.showTicker()
                    self.slider.setTickerPosition(cur_time)
                    self.model.setStoredDuration(cur_time)
                self.logData(charName, True, slot[0])
                self.mediaPlayer.setPosition(slot[0])
                return
            self.alert(self.model.isWindows, f"No scene found for {charName.title()} after current scene!")
            self.logData(charName, False, -1)
        return forward
    
    def logData(self, charName: str, success: bool, newTimestamp: int) -> str:
        data = {
            "e_name": "CharSmartForwardButtonPressed",
            "char_name": charName,
            "current_timestamp": self.mediaPlayer.position(),
            "new_timestamp": newTimestamp,
            "success": success
        }
        self.logger.log(data)

    def title(self) -> str:
        return "Smart Forward"
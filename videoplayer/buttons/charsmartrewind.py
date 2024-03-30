from .base import Button
from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
import winsound
from .hoverbutton import HoverButton, HoverButtonAction
import sys

class CharacterSmartRewindButton(HoverButton):
    def __init__(self, mediaPlayer, positionSlider) -> None:
        icon = QtGui.QIcon(QFileInfo(__file__).absolutePath() + '/../assets/charsmartrewindicon.ico')
        super().__init__(icon, mediaPlayer, positionSlider)

    def setup(self, model):
        self.model = model
        self.char_slots = self.model.get_char_timeslots()
        action_list = []
        for char_name, slots in self.char_slots.items():
            action_list.append(HoverButtonAction(char_name.title(), self.smartRewind(slots)))
        self.setOptions(action_list)
        self.setEnabled(True)

    def smartRewind(self, slots):
        def rewind():
            cur_time = self.model.getCurrentDuration()
            for slot in reversed(slots):
                if slot[1] >= cur_time:
                    continue
                if not self.slider.isTickerVisible():
                    self.slider.showTicker()
                    self.slider.setTickerPosition(cur_time)
                    self.model.setStoredDuration(cur_time)
                self.mediaPlayer.setPosition(slot[0])
                return
            self.alert(self.model.isWindows)
        return rewind
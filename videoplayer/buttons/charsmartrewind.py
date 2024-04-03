from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo
from .hoverbutton import HoverButton, HoverButtonAction

class CharacterSmartRewindButton(HoverButton):
    def __init__(self, mediaPlayer, positionSlider, logger) -> None:
        icon = QtGui.QIcon(QFileInfo(__file__).absolutePath() + '/../assets/charsmartrewindicon.ico')
        super().__init__(icon, mediaPlayer, positionSlider, logger)

    def setup(self, model):
        self.model = model
        self.char_slots = self.model.get_char_timeslots()
        action_list = []
        for char_name, slots in self.char_slots.items():
            action_list.append(HoverButtonAction(char_name.title(), self.smartRewind(char_name, slots)))
        self.setOptions(action_list)
        self.setEnabled(True)

    def smartRewind(self, char_name, slots):
        def rewind():
            cur_time = self.model.getCurrentDuration()
            for slot in reversed(slots):
                if slot[1] >= cur_time:
                    continue
                if not self.slider.isTickerVisible():
                    self.slider.showTicker()
                    self.slider.setTickerPosition(cur_time)
                    self.model.setStoredDuration(cur_time)
                self.log_data(char_name, True, slot[0])
                self.mediaPlayer.setPosition(slot[0])
                return
            self.alert(self.model.isWindows)
            self.log_data(char_name, False, -1)
        return rewind
    
    def log_data(self, char_name: str, success: bool, new_timestamp: int) -> str:
        data = {
            "e_name": "CharSmartRewindButtonPressed",
            "char_name": char_name,
            "current_timestamp": self.mediaPlayer.position(),
            "new_timestamp": new_timestamp,
            "success": success
        }
        self.logger.log(data)
import platform
from PyQt5.QtCore import QSettings, pyqtSignal, QObject
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Subtitle:
    """
    A class to represent a subtitle.

    ...

    Attributes
    ----------
    start : int
        time from when the subtitle should be visible
    end : int
        time from when the subtitle should be hidden
    text : str
        text to display when subtitle is visible

    """
    start: int
    end: int
    text: str

class Model(QObject):
    # Signals
    alertSignal = pyqtSignal(str)
    populateTimestampSignal = pyqtSignal()
    updateForwardCardsSignal = pyqtSignal()
    updateRewindCardsSignal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.currentDuration = 0
        self.totalDuration = 0
        self.storedDuration = 0
        self.isWindows = platform.system() == "Windows"
        self.settings = QSettings("pyqt_settings.ini", QSettings.IniFormat)
        self.lastFolderOpened = self.settings.value("LastFolder")
        self.subtitles = []
        self.isSubtitlesEnabled = False
        self.currentChosenCharacter = ""
        self.isForwardPanelClicked = False # if not, then assume backward panel

    def getLastOpenedFolder(self) -> str:
        return self.lastFolderOpened
    
    def setLastOpenedFolder(self, folder: str) -> None:
        self.lastFolderOpened = folder
        self.settings.setValue("LastFolder", self.lastFolderOpened)

    def setCurrentDuration(self, currentDuration: int):
        self.currentDuration = currentDuration

    def setTotalDuration(self, totalDuration: int):
        self.totalDuration = totalDuration

    def setStoredDuration(self, storedDuration: int):
        self.storedDuration = storedDuration

    def convertToMS(self, hours: int, minutes: int, seconds: int, milliseconds: int) -> int:
        return hours*60*60*1000 + minutes*60*1000 + seconds*1000 + milliseconds

    def setSubtitles(self, subtitles):
        self.subtitles = []
        self.middle_index = 0
        for subtitle in subtitles:
            self.subtitles.append(
                Subtitle(
                    self.convertToMS(subtitle.start.hours, subtitle.start.minutes, subtitle.start.seconds, subtitle.start.milliseconds),
                    self.convertToMS(subtitle.end.hours, subtitle.end.minutes, subtitle.end.seconds, subtitle.end.milliseconds),
                    subtitle.text
                )
            )
        self.middle_index = len(self.subtitles)//2

    def setSubtitlesEnabled(self, isEnabled: bool):
        self.isSubtitlesEnabled = isEnabled

    # Converts milliseconds to format "HH:MM:SS"
    def convertToHHMMSS(self, millseconds: int) -> str:
        seconds, _ = divmod(millseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:d}:{minutes:02d}:{seconds:02d}"
    
    def getCurrentDurationStr(self) -> str:
        return self.convertToHHMMSS(self.currentDuration)
    
    def getCurrentDuration(self) -> int:
        return self.currentDuration
    
    def getTotalDurationStr(self) -> str:
        return self.convertToHHMMSS(self.totalDuration)
    
    def getTotalDuration(self) -> int:
        return self.totalDuration
    
    def getTimeLabelStr(self):
        return f"{self.getCurrentDurationStr()} / {self.getTotalDurationStr()}"
        
    def getStoredDuration(self) -> int:
        return self.storedDuration
    
    def setCurrentChosenCharacter(self, char_name):
        self.currentChosenCharacter = char_name

    def setIsForwardPanelClicked(self, isClicked: bool):
        self.isForwardPanelClicked = isClicked
    
    def setTimeslots(self, data):
        self.characterTimeslots = []
        self.scene_timeslots = []
        self.characterTimeslots = data["CHAR"]
        self.scene_timeslots = data["SEG"]

    def getCharTimeslots(self) -> Dict[str, List[List[int]]]:
        return self.characterTimeslots
        
    def getSceneTimeslots(self):
        return self.scene_timeslots
    
    def getCurrentSubtitle(self) -> str:
        '''
        Calculates the current subtitle using the current timestamp.

                Returns:
                        subtitle (str): text of the subtitle
        '''
        if not self.isSubtitlesEnabled:
            return ""
        if len(self.subtitles) <= 0:
            return ""
        # binary search
        left = 0
        right = len(self.subtitles)-1
        while left <= right:
            middle = (left + right)//2
            subtitle = self.subtitles[middle]
            if self.currentDuration >= subtitle.start and self.currentDuration <= subtitle.end:
                return subtitle.text
            if self.currentDuration < subtitle.start:
                right = middle-1
                continue
            left = middle+1
        return ""
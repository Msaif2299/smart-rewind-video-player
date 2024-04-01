import platform
from PyQt5.QtCore import QSettings

class Model:
    def __init__(self) -> None:
        self.currentDuration = 0
        self.totalDuration = 0
        self.storedDuration = 0
        self.isWindows = platform.system() == "Windows"
        self.settings = QSettings("pyqt_settings.ini", QSettings.IniFormat)
        self.lastFolderOpened = self.settings.value("LastFolder")

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
    
    def setTimeslots(self, data):
        self.character_timeslots = []
        self.scene_timeslots = []
        self.character_timeslots = data["CHAR"]
        self.scene_timeslots = data["SEG"]

    def get_char_timeslots(self):
        return self.character_timeslots
        
    def getSceneTimeslots(self):
        return self.scene_timeslots
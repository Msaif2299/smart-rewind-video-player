class Model:
    def __init__(self) -> None:
        self.currentDuration = 0
        self.totalDuration = 0

    def setCurrentDuration(self, currentDuration: int):
        self.currentDuration = currentDuration

    def setTotalDuration(self, totalDuration: int):
        self.totalDuration = totalDuration

    # Converts milliseconds to format "HH:MM:SS"
    def convertToHHMMSS(self, millseconds: int) -> str:
        seconds, _ = divmod(millseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:d}:{minutes:02d}:{seconds:02d}"
    
    def getCurrentDurationStr(self) -> str:
        return self.convertToHHMMSS(self.currentDuration)
    
    def getTotalDurationStr(self) -> str:
        return self.convertToHHMMSS(self.totalDuration)
    
    def getTimeLabelStr(self):
        return f"{self.getCurrentDurationStr()} / {self.getTotalDurationStr()}"
        
    
    def setTimeslots(self, data):
        self.character_timeslots = data["CHAR"]
        self.scene_timeslots = data["SEG"]

    def get_char_timeslot(self, char_name):
        pass
        
    def get_scene_timeslot(self, current_timestamp):
        pass
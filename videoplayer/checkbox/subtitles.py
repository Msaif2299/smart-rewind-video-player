from PyQt5.QtWidgets import QCheckBox

class SubtitleCheckBox(QCheckBox):
    def __init__(self, model, logger):
        super().__init__()
        self.model = model
        self.logger = logger
        self.setText("Enable Subtitles")
        self.setEnabled(False)
        self.setStyleSheet("text-decoration: line-through;")

    def enableCheckBox(self):
        self.setEnabled(True)
        self.setStyleSheet("text-decoration: none;")
        self.stateChanged.connect(self.changeState)

    def changeState(self, _) -> None:
        self.model.setSubtitlesEnabled(self.isChecked())
        data = {
            "e_name": "SubtitleCheckBoxChecked",
            "is_checked": self.isChecked(),
            "current_timestamp": self.model.getCurrentDuration()
        }
        self.logger.log(data)

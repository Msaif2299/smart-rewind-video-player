from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtCore import QObject, Qt

class VideoSurface(QVideoWidget):

    def __init__(self, parent: QObject|None):
        super().__init__(parent)
        self.label = QLabel(self)
        self.initSubtitleLabel()

    def initSubtitleLabel(self):
        self.label.setStyleSheet("""
            background-color: rgba(5, 5, 5, 80);
            color: white;
            padding: 10px;
            font-size: 16pt;
        """)
        self.label.setVisible(False)

    def hideText(self):
        self.label.setVisible(False)

    def setText(self, text):
        self.label.setText(text)
        self.label.setVisible(True)

    def getLayout(self) -> QGridLayout:
        layout = QGridLayout()
        layout.addWidget(self, 0, 0)
        layout.addWidget(self.label, 0, 0, Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)
        return layout

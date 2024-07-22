from __future__ import annotations
from typing import TYPE_CHECKING
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QStyle
if TYPE_CHECKING:
    from videoplayer.model import Model

"""
Icon and text label: https://stackoverflow.com/questions/10533838/displaying-a-standard-icon-and-text-in-qlabel
    
"""

class AlertLabel(QWidget):
    IconSize = QSize(16, 16)
    HorizontalSpacing = 2
    def __init__(self, model: Model):
        super(QWidget, self).__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        icon_img = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
        self.icon = QLabel()
        self.icon.setPixmap(icon_img.pixmap(self.IconSize))
        self.icon.setVisible(False)
        self.label = QLabel()
        layout.addWidget(self.icon, alignment=Qt.AlignLeft)
        layout.addSpacing(self.HorizontalSpacing)
        layout.addWidget(self.label, alignment=Qt.AlignLeft)
        layout.addStretch()

        self.model = model
        self.model.alertSignal[str].connect(self.setText)
        self.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
        
    def setText(self, a0: str|None):
        if a0 is not None and len(a0) > 0:
            self.icon.setVisible(True)
            self.label.setText(a0)
            return
        self.icon.setVisible(False)
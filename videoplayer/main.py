from PyQt5.QtWidgets import QApplication

import sys

from model import Model
from controller import Controller
from viewer import Viewer
from eventlogger import Logger

app = QApplication(sys.argv)
model = Model()
logger = Logger("./videoplayer/logs")
logger.start()
controller = Controller(model, logger)
player = Viewer(controller, app, logger)
player.resize(640, 480)
player.show()
sys.exit(app.exec_())
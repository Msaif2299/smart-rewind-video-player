from PyQt5.QtWidgets import QApplication

import sys

from model import Model
from controller import Controller
from viewer import Viewer
from eventlogger import Logger, ErrorLogger
import os

def main():
    exitCode = 0
    if not os.path.isdir("./videoplayer"):
        os.mkdir("./videoplayer")
    errorLogger = ErrorLogger("./videoplayer/errorlogs")
    errorLogger.start()
    try:
        app = QApplication(sys.argv)
        model = Model()
        logger = Logger("./videoplayer/logs")
        logger.start()
        try:
            controller = Controller(model, logger)
            player = Viewer(controller, app, logger, errorLogger)
            player.resize(640, 480)
            player.show()
            exitCode = app.exec_()
        except Exception as e:
            print(f"Exception encountered: {e}")
            logger.stop()
            errorLogger.stop()
            sys.exit(exitCode)
    except Exception as e:
        print(f"Outer Exception encountered: {e}")
        errorLogger.stop()
        sys.exit(1)
    logger.stop()
    errorLogger.stop()
    sys.exit(exitCode)

if __name__ == '__main__':
    main()
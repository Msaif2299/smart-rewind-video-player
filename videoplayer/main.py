"""
Code Source: https://pythonprogramminglanguage.com/pyqt5-video-widget/
"""

from PyQt5.QtWidgets import QApplication

import sys

from model import Model
from controller import Controller
from viewer import Viewer
from eventlogger import Logger, ErrorLogger
import os
import traceback

def main():
    exitCode = 0
    logsFolder = "./logs"
    if not os.path.isdir(logsFolder):
        os.mkdir(logsFolder)
    errorLogger = ErrorLogger(logsFolder+"/error_logs")
    errorLogger.start()
    try:
        app = QApplication(sys.argv)
        model = Model()
        logger = Logger(logsFolder+"/event_logs")
        logger.start()
        try:
            controller = Controller(model, logger)
            player = Viewer(controller, app, logger, errorLogger)
            player.showMaximized()
            player.show()
            exitCode = app.exec_()
        except Exception as e:
            print(f"App Exception encountered: {traceback.format_exc()}")
            logger.stop()
            errorLogger.stop()
            sys.exit(exitCode)
    except Exception as e:
        print(f"System Exception encountered: {traceback.format_exc()}")
        errorLogger.stop()
        sys.exit(1)
    logger.stop()
    errorLogger.stop()
    sys.exit(exitCode)

if __name__ == '__main__':
    main()
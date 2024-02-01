import ui
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainUI = ui.MainUI()

    sys.exit(mainUI.run())
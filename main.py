import ui
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainUI = ui.MainUI()
    mainUI.update_forecast_ui()


    sys.exit(mainUI.run())
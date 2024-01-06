import PyQt5.QtWidgets as QtWidgets
import forecast
import time


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.forecast = forecast.Forecast()

        self.setWindowTitle('Weather Oracle')
        self.setGeometry(100, 100, 300, 600)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QHBoxLayout()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: lightblue;")
        self.day_list = []
        for i in range(7):
            current = DayUI()
            self.layout.addWidget(current)
            self.day_list.append(current)

        self.central_widget.setLayout(self.layout)

    def update_forecast_ui(self):
        self.forecast.update_data()
        dates, temp = self.forecast.get_dates_and_temp()
        for i in range(7):
            self.day_list[i].set_label_top(str(dates[7 + i]))
            self.day_list[i].set_label_bottom(str(temp[7 + i]))

    def run(self):
        self.show()
        return QtWidgets.QApplication.instance().exec_()



class DayUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.day_layout = QtWidgets.QVBoxLayout()

        # Creating labels
        self.label_top = QtWidgets.QLabel("Default Top Text")
        self.label_bottom = QtWidgets.QLabel("Default Bottom Text")

        # Adding labels to the layout
        self.day_layout.addWidget(self.label_top)
        self.day_layout.addWidget(self.label_bottom)

        # Setting the layout for the widget
        self.setLayout(self.day_layout)
        self.day_layout.setSpacing(0)

        # Setting the background color for the entire widget
        self.setStyleSheet("background-color: lightgreen;")

    def set_label_top(self, text):
        self.label_top.setText(text)

    def set_label_bottom(self, text):
        self.label_bottom.setText(text)








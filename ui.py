import PyQt5.QtWidgets as ui
import time
import api

class MainUI:
    def __init__(self):
        self.requests = api.Requests()
        self.app = ui.QApplication([])
        self.window = ui.QWidget()
        self.window.setWindowTitle('Weather Oracle')
        self.layout = ui.QHBoxLayout()

        self.day_list = []
        for i in range(7):
            current = DayUI("blank", "blank")
            self.layout.addWidget(current.get_widget())
            self.day_list.append(current)


        self.testlabel = ui.QLabel("test")
        self.layout.addWidget(self.testlabel)

        self.window.setLayout(self.layout)




    def update_forecast(self):
        for i in range(7):
            data = self.requests.list_day(i)
            self.day_list[i].set_labeltop(str(data[0]))
            self.day_list[i].set_labelbot(str(data[1]))
    def show(self):
        self.window.show()
        self.app.exec()


class DayUI:
    def __init__(self, text1, text2):
        self.day = ui.QWidget()
        self.day_layout = ui.QVBoxLayout()
        self.labeltop = ui.QLabel(text1)
        self.day_layout.addWidget(self.labeltop)
        self.labelbot = ui.QLabel(text2)
        self.day_layout.addWidget(self.labelbot)
        self.day.setLayout(self.day_layout)
    def get_widget(self):
        return self.day

    def set_labeltop(self, text):
        self.labeltop.setText(text)

    def set_labelbot(self, text):
        self.labelbot.setText(text)





# while True:
#     time.sleep(1)
#     label.setText("test {}".format(i))
#     i += 1




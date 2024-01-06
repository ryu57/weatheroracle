import api
import model
import datetime

class Forecast:
    def __init__(self):
        self.requests = api.Requests()
        self.modeleval = model.ModelEvaluator()
        self.dates = []
        self.temps = []

    def update_data(self):
        self.dates = []
        self.temps = []

        # History
        for i in range(7):
            self.dates.append(datetime.datetime.strptime(self.requests.historical_data["forecast"]['forecastday'][i]['date'],"%Y-%m-%d").date())
            self.temps.append(
                self.requests.historical_data["forecast"]['forecastday'][i]['day'][
                    'avgtemp_c'])

        # Provided forecast for first 3 days
        for i in range(3):
            self.dates.append(datetime.datetime.strptime(self.requests.data["forecast"]['forecastday'][i]['date'],"%Y-%m-%d").date())
            self.temps.append(self.requests.data["forecast"]['forecastday'][i]['day']['avgtemp_c'])

        # Predicted forecast for 4 next days
        for i in range(4):
            pred = self.modeleval.evaluate(self.list_n_temp(i, i + 10))
            last_date = self.dates[-1]
            current_date = last_date + datetime.timedelta(days=1)
            self.temps.append(pred)
            self.dates.append(current_date)

    def get_dates_and_temp(self):
        return self.dates, self.temps

    def list_n_temp(self, begin_index, end_index):
        """
        Get a list of the api temperatures

        begin_index = 7, end_index = 10 for forecast days

        :param begin_index: index of the first element
        :param end_index: index of the last element
        :return: returns the temperature list
        """
        return self.temps[begin_index:end_index]
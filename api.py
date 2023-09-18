import requests
import json
import datetime

class Requests:
    def __init__(self):
        try:
            with open('forecast.json', 'r') as infile:
                self.data = json.load(infile)
        except:
            self.get_new_forecast()
        try:
            with open('history.json', 'r') as infile:
                self.historical_data = json.load(infile)
        except:
            self.get_new_forecast()

    def get_new_forecast(self):
        api = "http://api.weatherapi.com/v1/forecast.json?"
        key = "key=28b5a01635e94ca99ec182217232407"
        query = "&q=Toronto"
        days = "&days=7"
        final = api + key + query + days

        response = requests.get(final)
        data = response.json()

        with open('forecast.json', 'w') as outfile:
            json.dump(data, outfile)
        self.data = data

    def get_new_history(self):
        api = "http://api.weatherapi.com/v1/history.json?"
        key = "key=28b5a01635e94ca99ec182217232407"
        query = "&q=Toronto"
        date_end = datetime.date.today() - datetime.timedelta(days=1)
        date_start = datetime.date.today() - datetime.timedelta(days=7)
        day_start = f"&dt={date_start}"
        day_end = f"&end_dt={date_end}"
        final = api + key + query + day_start + day_end

        response = requests.get(final)
        data = response.json()

        with open('history.json', 'w') as outfile:
            json.dump(data, outfile)
        self.data = data

    def list_day(self,day_num):
        return (self.data["forecast"]['forecastday'][day_num]['date'],self.data["forecast"]['forecastday'][day_num]['day']['avgtemp_c'])

    def list_history(self):
        arr = []
        for i in range(7):
            arr.append(self.historical_data["forecast"]['forecastday'][i]['day']['avgtemp_c'])
        return arr




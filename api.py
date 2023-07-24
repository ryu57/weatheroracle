import requests
import json

class Requests:
    def __init__(self):
        try:
            with open('forecast.json', 'r') as infile:
                self.data = json.load(infile)
        except:
            print("No Forecast file")

    def get_new(self):
        api = "http://api.weatherapi.com/v1/forecast.json?"
        key = "key=28b5a01635e94ca99ec182217232407"
        query = "&q=Toronto"
        days = "&days=7"
        final = api + key + query + days

        response = requests.get(final)
        data = response.json()

        with open('forecast.json', 'w') as outfile:
            json.dump(data, outfile)
        self.data = json.load(data)

    def list_day(self,day_num):
        return (self.data["forecast"]['forecastday'][day_num]['date'],self.data["forecast"]['forecastday'][day_num]['day']['avgtemp_c'])




import requests
import time
import json
import pandas as pd
from settings import *


month_ms = 2629743000
ms_200_candles = int(INTERVAL) * 200 * 60000
start_time = int(time.time()* 1000 - MONTHS * month_ms)
end_time = int(time.time() * 1000)


class Data: 

    def _query_data(start):
        url = "https://api.bybit.com/derivatives/v3/public/kline"
        params = {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "start": start,
            "end": end_time
        }
        response = requests.get(url, params=params)
        data = response.json()
        try:return data['result']["list"]
        except: return None

    @classmethod
    def _get_data(cls):
        start = start_time
        end = end_time
        data = [i for i in cls._query_data(start)][::-1]
        start+=ms_200_candles

        while end>start+ms_200_candles:
            block = cls._query_data(start)
            for i in block[::-1]: data.append(i)
            start+=ms_200_candles
        return data

    def write_historical_data(file_name):
        data = {'candles': [i for i in Data._get_data()]}
        json_data = json.dumps(data)
        try:
            f = open(file_name, "w")
            f.write(json_data)
            f.close()
        except FileNotFoundError: 
            print(f"File {file_name} not found")

    def read_historical_data(file_name):

        try: 
            f = open(file_name)
            data = json.load(f)
            f.close()
            return data["candles"]
        except FileNotFoundError:
            return f"File {file_name} not found"

    def format_to_df(data_):
            
        data = pd.DataFrame(data_)
        data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Turnover']  # specify columns
        data = data.astype(float)
        data = data.set_index('Time') 
        data.index = pd.to_datetime(data.index, unit='ms')
        

        return data




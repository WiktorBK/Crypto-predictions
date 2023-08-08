import time
import json
import pandas as pd
from settings import *
import yfinance as yf


class Data: 

    @classmethod
    def get_data(cls):
        BTC_Ticker = yf.Ticker("BTC-USD")
        BTC_data = BTC_Ticker.history(period="max")
        BTC_data.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)

        return BTC_data





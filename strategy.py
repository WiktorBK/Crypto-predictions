from ta.trend import EMAIndicator, PSARIndicator, MACD
from ta.volatility import AverageTrueRange, bollinger_hband, bollinger_lband
from ta.momentum import RSIIndicator
import pandas_ta as ta
from settings import *
import pandas as pd


class TechnicalAnalysis:

    def ema_difference(df):
        ema_difference = []
        df[f'ema{EMA1}'] = ta.ema(df['Close'], length=EMA1)
        df[f'ema{EMA2}'] = ta.ema(df['Close'], length=EMA2)
        
        # Calculate difference between two emas and append to a list
        for i in range(len(df[f'ema{EMA2}'])):
            ema_difference.append(df[f'ema{EMA2}'][i] - df[f'ema{EMA1}'][i])
        return ema_difference
        
    def macd_difference(df):
        try: return MACD(df['Close']).macd_diff()
        except Exception as e: return f"Couldn't calculate macd difference: \n {e}"

    def ema_price(df):
        try: return ta.ema(df['Close'], length=EMA1)
        except Exception as e: return f"Couldn't calculate ema price:\n {e}"

    def average_true_range(df):
        try: return AverageTrueRange(df['High'], df["Low"], df['Close'], 14).average_true_range()
        except Exception as e: return f"Couldn't calculate average true range: \n {e}"

    def rsi_indicator(df):
        try: return RSIIndicator(df['Close'], 14).rsi()
        except Exception as e: return f"Couldn't calculate RSI: \n {e}"

    def in_uptrend(df):
        up_trend = []
        df[f'ema{EMA1}'] = EMAIndicator(df['Close'], EMA1).ema_indicator()
        
        for i in range(len(df[f'ema{EMA1}'])):
            if df[f'ema{EMA1}'][i] <= df['Close'][i]:
                up_trend.append(1)
            else:
                up_trend.append(0)
        return up_trend

    def psar_price(df):
        df['psar_down'] = PSARIndicator(df['High'], df["Low"], df['Close']).psar_down()
        psar = []

        for i in df['psar_down']:
            if pd.isna(i): psar.append(1)
            else: psar.append(0)

        return psar


import pandas as pd
import numpy as np
import ta
from utils import *


class DataRepo():
    def __init__(self):
        self.df = None

    def data_cleaning(self):
        data = pd.read_csv("https://raw.githubusercontent.com/khanabdullah9/NIFTY_50_DS/master/Nifty%2050%20Historical%20Data.csv")
        
        df = data.copy()
        df.columns = ["Date","Price","Open","High","Low","Vol","Change_%"]
        vol_series = df["Vol"] #extra copy


        df["Date"] = pd.to_datetime(df["Date"], format = "%d-%m-%Y")
        df["Price"] = df["Price"].apply(remove_symbols).astype("float")
        df["Open"] = df["Open"].apply(remove_symbols).astype("float")
        df["High"] = df["High"].apply(remove_symbols).astype("float")
        df["Low"] = df["Low"].apply(remove_symbols).astype("float")
        df["Vol"] = df["Vol"].apply(remove_symbols).astype("float")
        df["Change_%"] = df["Change_%"].apply(remove_symbols).astype("float")

        df = df.sort_values(by = "Date")

        #Feature engineering
        prev_date = df["Date"].shift(1)
        df["day_lag"] = (df["Date"] - prev_date).dt.days

        df["Vol_Multiple"] = vol_series.apply(extract_chars)

        future_value = df["Price"].shift(-1)
        difference = (future_value - df["Price"]) / df["Price"]
        df["Difference"] = difference

        df["SMA_5"] = df["Price"].rolling(5).mean()
        df["SMA_5"] = df["SMA_5"].bfill()

        df["SMA_20"] = df["Price"].rolling(20).mean()
        df["SMA_20"] = df["SMA_20"].bfill()

        df["RSI_14"] = ta.momentum.rsi(df["Price"], window=14)
        df["RSI_14"] = df["RSI_14"].bfill()

        df["MACD"] = ta.trend.macd(df["Price"])
        df["MACD"] = df["MACD"].bfill()

        df["MACD_signal"] = ta.trend.macd_signal(df["Price"])
        df["MACD_signal"] = df["MACD_signal"].bfill()

        df["MACD_diff"] = ta.trend.macd_diff(df["Price"])
        df["MACD_diff"] = df["MACD_diff"].bfill()

        df["ATR"] = ta.volatility.average_true_range(df["High"], df["Low"], df["Price"])

        df["Price_lag1"] = df["Price"].shift(1)
        df["Price_lag3"] = df["Price"].shift(3)
        df["Price_lag7"] = df["Price"].shift(7)

        df["Return_1"] = df["Price"].pct_change(1)
        df["Return_3"] = df["Price"].pct_change(3)
        df["Return_7"] = df["Price"].pct_change(7)


        # Target variable (0 -> STABLE OR DOWN, 2 -> UP)
        df["Target"] = np.where(
            difference > 0, 1, 0
        )

        df = df.dropna()

        self.df = df

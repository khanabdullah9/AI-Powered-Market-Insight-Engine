import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng
from data_repo import DataRepo
from utils import plot_macd, plot_rsi, plot_feature
import datetime
from predictor import Predictor

data_repo = DataRepo()
data_repo.data_cleaning()
df = data_repo.df

MIN_DATE = datetime.date(1900, 1, 1) 
MAX_DATE = datetime.date.today() 

dt_col1, dt_col2, btn_col = st.columns(3)
st.set_page_config(layout="wide")

with dt_col1:
    start_date = st.date_input("Start", min_value = MIN_DATE, max_value = MAX_DATE)
with dt_col2:
    end_date = st.date_input("End", min_value = MIN_DATE, max_value = MAX_DATE)

if start_date and end_date and (df.shape[0] > 0):
    str_start = start_date.strftime("%Y-%m-%d"); str_end = end_date.strftime("%Y-%m-%d")

    df_col1, pred_col = st.columns(2)
    with df_col1:
        table = df[["Date","Price","Open","High","Low","Target"]].tail(5)
        table["Target"] = table["Target"].map({0:"Fall",1:"Rise"})
        table.columns = ["Date","Price","Open","High","Low","Movement"]

        st.dataframe(table, hide_index = True, column_config={
        "Date": st.column_config.DateColumn(
            "Date",
            format="DD-MM-YYYY", # You can customize the format
        )
    })
    with pred_col:
        predictor_model = Predictor(df)
        prediction = predictor_model.predict()
        print(f"pred = {prediction}")
        st.write("Predicted Movement")
        st.badge("Rise" if prediction == 1 else "Fall")

    plot_macd(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), df)
    plot_rsi(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), df)
    plot_feature(str_start, str_end, df, ["Change_%"])

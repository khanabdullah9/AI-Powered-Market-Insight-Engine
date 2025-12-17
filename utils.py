import pandas as pd
import streamlit as st
import altair as alt

#Utility functions
def remove_symbols(x):
  x = remove_chars(x)
  return x.replace(",","").replace("%","")
  # .replace("M","").replace("B","")

def remove_chars(x):
  chars = [chr(i) for i in range(65, 65+26)]
  x = str(x)
  for c in x:
    if c in chars:
      x = x.replace(c,"")
  return x

def extract_chars(x):
  chars = [chr(i) for i in range(65, 65+26)]
  x = str(x)
  for c in x:
    if c in chars:
      return c
  return ""


def create_target_var(df):
  for idx, row in df.iterrows():
    if idx == 0:
      continue

    lag_value = df["Price"].shift(idx-1)
    curr_val = df["Price"]
    difference = curr_val - lag_value

    if difference == 0:
      df["Target"] =  0 #Stable
    elif difference > 0:
      df["Target"] =  1 #Up
    else:
      df["Target"] = -1 #Down

def chronological_split(df, features, target, train_percent=0.8):
  """Unlike scikit-learn's train-test split this function creates split maintaining the chronological order
  (Crucial for time series data)"""
  train_size = int(len(df) * train_percent)

  train = df.iloc[:train_size]
  test = df.iloc[train_size:]

  X_train = train[features].copy()
  y_train = train[target].copy()

  X_test = test[features].copy()
  y_test = test[target].copy()

  # ensure 1-D arrays
  y_train = y_train.values.ravel()
  y_test = y_test.values.ravel()

  return X_train, X_test, y_train, y_test

def download_performance(y_test, y_pred):
  performance = {
    "Actual": y_test,
    "Predicted": y_pred
}
  performance = pd.DataFrame(performance)
  performance.to_csv("performance.csv")

def save_report(report, row, index):
  match_count = 0 if (report.shape[0] == 0) else report[report["name"] == row["name"]].shape[0]
  if match_count == 1: # avoiding multiple entries
    return report

  return pd.concat([report, pd.DataFrame(row, index = [index])])

def get_report_val(name, col):
#   return report[report["name"] == name][col].to_numpy()[0]
    pass

def plot_macd(start_date, end_date, df):
  if df is None:
    return
  filtered_df = df[(df.Date >= start_date) & (df.Date <= end_date)]
  filtered_df = filtered_df[["Date","MACD","MACD_signal","MACD_diff"]]
  st.line_chart(filtered_df, x = "Date", y = ["MACD","MACD_signal","MACD_diff"])

def plot_rsi(start_date, end_date, df):
  if df is None:
    return
  filtered_df = df[(df.Date >= start_date) & (df.Date <= end_date)]
  filtered_df = filtered_df[["Date","RSI_14"]]
  st.line_chart(filtered_df, x = "Date", y = "RSI_14")

def plot_feature(start_date, end_date, df, feature_list):
  if df is None:
    return
  filtered_df = df[(df.Date >= start_date) & (df.Date <= end_date)]
  filtered_df = filtered_df[feature_list + ["Date"]]
  st.line_chart(filtered_df, x = "Date", y = feature_list)

def plot_feature_altair(start_date, end_date, df, feature_list):
  filtered_df = df[(df.Date >= start_date) & (df.Date <= end_date)]

  for feature in feature_list:
      chart = (
          alt.Chart(filtered_df)
          .mark_line()
          .encode(
                x="Date:T",
                y=alt.Y(f"{feature}:Q", title=feature)
          )
          .properties(height=300)
          .interactive(False)   # 🔴 disables zoom & pan
        )

      st.altair_chart(chart, use_container_width=True)

  
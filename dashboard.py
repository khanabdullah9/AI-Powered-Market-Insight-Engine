import streamlit as st
import pandas as pd
import datetime
# Assuming data_repo, Predictor, and utils functions are in files named data_repo.py, predictor.py, and utils.py
from data_repo import DataRepo
from utils import plot_feature
from predictor import Predictor

# --- CONFIGURATION (MUST be the first Streamlit command) ---
st.set_page_config(
    layout="wide",
    page_title="Stock Movement Predictor",
    menu_items={'About': "A simple stock prediction dashboard."}
)

st.warning(
    f"⚠️ **Maintenance Notice:** This application is no longer actively maintained. "
    f"The last data update and code review was on **December 17th, 2025**. "
    f"The predictions should be used for historical analysis only, not for live trading."
)

# --- INITIAL DATA SETUP ---
# Initialize classes (assuming these are defined in your local files)
data_repo = DataRepo()
data_repo.data_cleaning()
df = data_repo.df

MIN_DATE = datetime.date(1900, 1, 1) 
MAX_DATE = datetime.date.today() 

# Setting default values to match the screenshot for demonstration
DEFAULT_START_DATE = datetime.date(2024, 12, 10)
DEFAULT_END_DATE = datetime.date.today()

# --- HEADER AND DATE PICKERS ---
st.title("📈 Market Movement Analysis & Prediction (NIFTY 50)")

# Use 2 columns for clean date pickers
dt_col1, dt_col2 = st.columns(2)

with dt_col1:
    start_date = st.date_input(
        "Start", 
        min_value = MIN_DATE, 
        max_value = MAX_DATE, 
        value=DEFAULT_START_DATE
    )
with dt_col2:
    end_date = st.date_input(
        "End", 
        min_value = MIN_DATE, 
        max_value = MAX_DATE, 
        value=DEFAULT_END_DATE
    )

# --- MAIN DASHBOARD LOGIC ---
if start_date and end_date and (df.shape[0] > 0):
    str_start = start_date.strftime("%Y-%m-%d")
    str_end = end_date.strftime("%Y-%m-%d")

    # --- Dataframe Preparation ---
    # Use .copy() to avoid SettingWithCopyWarning
    table = df[["Date","Price","Open","High","Low","Target"]].tail(5).copy()
    table["Target"] = table["Target"].map({0:"Fall",1:"Rise"})
    table.columns = ["Date","Price","Open","High","Low","Movement"]
    
    # --- Conditional Styling Function (Pandas Styler Fix) ---
    def style_movement(val):
        """Applies CSS style to the 'Movement' column based on value."""
        if val == "Rise":
            # Dark Blue background for Rise
            return 'background-color: #0047b3; color: white; font-weight: bold;'
        elif val == "Fall":
            # Dark Red background for Fall
            return 'background-color: #b30000; color: white; font-weight: bold;'
        return ''

    # Apply Styling with Pandas Styler
    styled_table = table.style.applymap(
        style_movement, 
        subset=['Movement'] # Apply the style ONLY to the 'Movement' column
    )
    
    # --- Table and Prediction Layout ---
    # Adjust column ratio: 1.5 for the table, 1 for the prediction metric
    df_col1, pred_col = st.columns([1.5, 1])
    
    # --- Display Table ---
    with df_col1:
        st.subheader("Historical Data Summary")
        # Render the STYLED table object
        st.dataframe(
            styled_table, 
            hide_index = True, 
            height=240, 
            column_config={
                "Date": st.column_config.DateColumn(
                    "Date",
                    format="DD-MM-YYYY",
                )
                # No column config for 'Movement' needed here since styling is handled by Styler
            }
        )

    # --- Display Prediction ---
    with pred_col:
        st.subheader("Next Day Prediction")
        
        # Get Prediction
        predictor_model = Predictor(df)
        prediction = predictor_model.predict()
        pred_text = "Rise" if prediction == 1 else "Fall"

        # Use st.metric for a clear, impactful display
        st.metric(
            label=f"Prediction for {DEFAULT_END_DATE.strftime("%d-%m-%Y")}", 
            value=pred_text, 
            # Use delta_color to reflect the market sentiment (Rise=Normal/Green, Fall=Inverse/Red)
            delta="Predicted by Model (F1-Score: 0.61)", 
            delta_color="normal" if prediction == 1 else "inverse"
        )
        # st.info("Model F1-Score: 0.61")

    # --- Plots/Visual Analysis Section ---
    st.markdown("---") # Visual separator
    st.header("Visual Technical Analysis")
    
    # Sub-headers for clarity above each plot
    st.subheader("MACD Crossover Plot")
    # plot_macd(str_start, str_end, df)
    plot_feature(str_start, str_end, df, ["MACD", "MACD_signal", "MACD_diff"])
    
    st.subheader("RSI (Relative Strength Index) Plot")
    # plot_rsi(str_start, str_end, df)
    plot_feature(str_start, str_end, df, ["RSI_14"])
    
    st.subheader("Price Change Feature")
    plot_feature(str_start, str_end, df, ["Change_%"])
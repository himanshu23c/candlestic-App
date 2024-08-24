code = """

import streamlit as st
import pandas as pd
from datetime import datetime
from bokeh.plotting import figure, column
import talib

st.set_page_config(layout="wide", page_title="Stock Dashboard")

@st.cache_data  # Change this from @st.catch_data to @st.cache_data
def load_dataset():
    apple_df = pd.read_csv('AAPL.csv', parse_dates=True)  # Ensure 'AAPL.csv' is in the correct directory
    apple_df['Date'] = pd.to_datetime(apple_df['Date'])
    apple_df['BarColor'] = apple_df[['Open', 'Close']].apply(lambda o: 'red' if o.Open > o.Close else 'green', axis=1)
    apple_df['Date_str'] = apple_df['Date'].astype(str)

    # Calculate indicators
    apple_df['SMA'] = talib.SMA(apple_df.Close, timeperiod=3)
    apple_df['MA'] = talib.MA(apple_df.Close, timeperiod=3)
    apple_df['EMA'] = talib.EMA(apple_df.Close, timeperiod=3)
    apple_df['WMA'] = talib.WMA(apple_df.Close, timeperiod=3)
    apple_df['RSI'] = talib.RSI(apple_df.Close, timeperiod=3)
    apple_df['MOM'] = talib.MOM(apple_df.Close, timeperiod=3)  # Fixed typo from 'tablib' to 'talib'
    apple_df['DEMA'] = talib.DEMA(apple_df.Close, timeperiod=3)
    apple_df['TEMA'] = talib.TEMA(apple_df.Close, timeperiod=3)

    return apple_df

apple_df = load_dataset()
indicator_colors = {'SMA': 'orange', 'EMA': 'blue', 'WMA': 'green', 'RSI': 'red', 'MOM': 'black', "DEMA": 'tomato', 'TEMA': 'dodgerblue'}

def create_chart(df, close_line=False, include_vol=False, indicators=[]):
    # Candlestick Pattern Logic
    candle = figure(x_axis_type='datetime', plot_height=500, x_range=(df.Date.values[0], df.Date.values[-1]),
                    tooltips=[("Date", "@Date_str"), ("Open", "@Open"), ("High", "@High"), ("Low", "@Low"), ("Close", "@Close")])
    
    candle.segment('Date', 'Low', 'Date', 'High', color='black', line_width=0.5, source=df)
    candle.segment('Date', 'Open', 'Date', 'Close', line_color='BarColor', line_width=2 if len(df) > 100 else 6, source=df)

    candle.xaxis.axis_label = 'Date'
    candle.yaxis.axis_label = 'Price($)'

    # Close price line
    if close_line:
        candle.line('Date', 'Close', color='black', line_width=1, source=df)

    for indicator in indicators:
        candle.line('Date', indicator, color=indicator_colors[indicator], line_width=2, source=df, legend_label=indicator)

    # Volume bar logic
    volume = None
    if include_vol:
        volume = figure(x_axis_type='datetime', plot_height=150, x_range=(df.Date.values[0], df.Date.values[-1]))
        volume.segment('Date', 0, 'Date', 'Volume', line_color='BarColor', line_width=2 if len(df) > 100 else 6, alpha=0.8, source=df)  # Fixed typo 'sagment' to 'segment'
        volume.yaxis.axis_label = 'Volume'

    return column(children=[candle, volume], sizing_mode='scale_width') if volume else candle

talib_indicators = ['MA', 'EMA', 'SMA', 'WMA', 'RSI', 'MOM', 'DEMA', 'TEMA']

# DASHBOARD
st.title('Apple Stock Dashboard :tea: ')

fig = create_chart(apple_df)
st.bokeh_chart(fig, use_container_width=True)


"""
with open("app.py", "w") as file:
    file.write(code)

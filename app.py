code = """
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# List of stocks for analysis
stock = ['HDFCBANK.NS', 'TCS.NS', 'RELIANCE.NS', 'ADANIPOWER.NS']

# Title of the app
st.title('Stock Market Candlestick Chart')

# User input for stock ticker from predefined list
ticker = st.selectbox('Select Stock Ticker', stock)

# User input for date range
start_date = st.date_input('Start Date', pd.to_datetime('2022-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('today'))

# Fetch stock data
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Plot candlestick chart
fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
             open=stock_data['Open'],
             high=stock_data['High'],
             low=stock_data['Low'],
             close=stock_data['Close'])])

# Add Moving Averages
stock_data['MA10'] = stock_data['Close'].rolling(window=10).mean()
stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()

fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA10'], mode='lines', name='MA10'))
fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA20'], mode='lines', name='MA20'))
fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MA50'], mode='lines', name='MA50'))

# Display the chart
st.plotly_chart(fig)
"""
with open("app.py", "w") as file:
    file.write(code)

import yfinance as yf
import streamlit as st

st.write("""
# Stock Price App

Shown are the stock **closing price** and ***volume*** of Tata Motors!

""")

tickerSymbol = 'TATAMOTORS.NS'
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2018-11-29', end='2023-11-28')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)
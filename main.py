import yfinance as yf
import streamlit as st
import datetime

st.write("""
# Stock Price App

Enter the stock symbol to see the closing price and volume!

""")

# Get the current date
current_date = datetime.datetime.now().strftime('%Y-%m-%d')

# User input for stock symbol
ticker_symbol = st.text_input('Enter Stock Symbol:')
if not ticker_symbol:
    st.warning('Please enter a valid stock symbol.')
    st.stop()


try:
    # Get data on the selected ticker
    ticker_data = yf.Ticker(ticker_symbol)
except ValueError:
    print("Invaild Data")
    st.warning('Please enter a valid stock symbol.')
    st.stop()



try:
    # Get the historical prices for the selected ticker
    ticker_df = ticker_data.history(period='1d', start='2018-11-29', end=current_date)
except ValueError:
    print("error")
    
    st.error('Error fetching data. Please check the stock symbol and try again.')
    st.stop()

# Display stock information
st.write(f"""
## Stock Information for {ticker_symbol}
""")

# tickerSymbol = 'TATAMOTORS.NS'
# #get data on this ticker
# tickerData = yf.Ticker(tickerSymbol)
# #get the historical prices for this ticker
# tickerDf = tickerData.history(period='1d', start='2018-11-29', end='2023-11-28')
# # Open	High	Low	Close	Volume	Dividends	Stock Splits


st.write("""
## Opening Price
""")
st.line_chart(ticker_df.Open)

st.write("""
## Closing Price
""")
st.line_chart(ticker_df.Close)





st.write("""
## Volume Price
""")
st.line_chart(ticker_df.Volume) 


if st.checkbox('Show Moving Average'):
    period = st.slider('Select Moving Average Period', min_value=1, max_value=50, value=20)
    ticker_df['MA'] = ticker_df['Close'].rolling(window=period).mean()
    st.line_chart(ticker_df[['Close', 'MA']])
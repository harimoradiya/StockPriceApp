import datetime
import yfinance as yf
import streamlit as st

st.write("""
# Stock Price App

Enter the stock symbol to see the closing price and volume!

""")

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
    st.error('Error fetching data. Please check the stock symbol and try again.')
    st.stop()

# Market status
if is_market_open():
    st.markdown("<h2 style='color: green;'>Open</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='color: red;'>Closed</h2>", unsafe_allow_html=True)

# Technical Indicators: Moving Averages
st.sidebar.subheader("Technical Indicators")
ma_period = st.sidebar.slider('Select MA Period', min_value=5, max_value=200, value=50, step=5)
ticker_df[f'MA_{ma_period}'] = ticker_df['Close'].rolling(window=ma_period).mean()

fig = go.Figure()

# Add the closing price as a line trace
fig.add_trace(go.Scatter(x=ticker_df.index, y=ticker_df['Close'], mode='lines', name='Close'))

# Update layout with title and axis labels
fig.update_layout(
    title=f'Stock Closing Price Chart for {ticker_symbol}',
    xaxis_title='Date',
    yaxis_title='Price'
)

# Add hover mode and tooltips
fig.update_traces(hoverinfo='x+y', line=dict(width=2))

# Show the interactive chart
st.plotly_chart(fig, use_container_width=True)

# Display the opening price chart
st.write("## Opening Price")
st.line_chart(ticker_df['Open'])

# Stock News
st.write("## Latest News")
news = ticker_data.news
print(f"news  - {news}")
for article in news[:8]:  # Display the latest 8 news articles
    title = article['title']
    publisher = article['publisher']
    link = article['link']
    publish_time = datetime.datetime.fromtimestamp(article['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')
    thumbnail_url = article.get('thumbnail', {}).get('resolutions', [{}])[0].get('url')

    st.write(f"### {title}")
    st.write(f"**Publisher:** {publisher}")
    st.write(f"**Published at:** {publish_time}")
    st.write(f"[Read more]({link})")

    if thumbnail_url:
        st.image(thumbnail_url, width=140)
    st.write("---")

# Financial Metrics
st.write("## Financial Metrics")
financials = ticker_data.info
st.write(f"**P/E Ratio:** {financials.get('trailingPE', 'N/A')}")
st.write(f"**EPS:** {financials.get('trailingEps', 'N/A')}")
st.write(f"**Market Cap:** {financials.get('marketCap', 'N/A')}")
st.write(f"**Dividend Yield:** {financials.get('dividendYield', 'N/A')}")

# Portfolio 
st.sidebar.write("## Portfolio Tracker")
with st.sidebar.form(key='portfolio_form'):
    stock_symbol = st.text_input("Stock Symbol").upper()
    buying_price = st.number_input("Buying Price", min_value=0.0, format="%.2f")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR", "JPY", "CNY", "AUD"])
    add_stock = st.form_submit_button(label='Add Stock to Portfolio')

    if add_stock:
        current_price = yf.Ticker(stock_symbol).history(period='1d')['Close'][-1]
        total_value = current_price * quantity

        # Append the new stock to the portfolio
        new_stock = pd.DataFrame({
            'Symbol': [stock_symbol],
            'Buying Price': [buying_price],
            'Quantity': [quantity],
            'Currency': [currency],
            'Current Price': [current_price],
            'Total Value': [total_value]
        })

        st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_stock], ignore_index=True)

# Display the portfolio
st.write("## Your Portfolio")
if not st.session_state.portfolio.empty:
    st.write(st.session_state.portfolio)
    st.write(f"**Total Portfolio Value:** ${st.session_state.portfolio['Total Value'].sum():,.2f}")
else:
    st.write("No stocks in the portfolio yet.")

# Alerts
st.sidebar.write("## Set Price Alert")
alert_price = st.sidebar.number_input("Alert if price goes below", min_value=0.0, value=100.0)
current_price = ticker_df['Close'][-1]
if current_price < alert_price:
    st.sidebar.write(f"**Alert:** {ticker_symbol} price is below ${alert_price}")

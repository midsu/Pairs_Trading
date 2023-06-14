import requests
import csv
from datetime import datetime

# Enter your Alpha Vantage API key here
api_key = 'R9RDVNKFONRCSA6D'

# Prompt the user to enter a stock ticker
stock_ticker = input('Enter a stock ticker to retrieve its data (e.g. AAPL): ')

# Make a request to the Alpha Vantage API to retrieve the stock data
response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock_ticker}&apikey={api_key}')

# Parse the response data as JSON
data = response.json()

# Check if the API returned an error message
if 'Error Message' in data:
    print(data['Error Message'])
else:
    # Extract the stock data as a list of tuples
    stock_data = []
    for date in data['Time Series (Daily)']:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%m/%d/%Y')
        open_price = float(data['Time Series (Daily)'][date]['1. open'])
        high_price = float(data['Time Series (Daily)'][date]['2. high'])
        low_price = float(data['Time Series (Daily)'][date]['3. low'])
        close_price = float(data['Time Series (Daily)'][date]['4. close'])
        volume = int(data['Time Series (Daily)'][date]['5. volume']) if '5. volume' in data['Time Series (Daily)'][date] else 0
        daily_change = close_price - open_price
        percent_change = (daily_change / open_price) * 100 if open_price != 0 else 0
        stock_data.append((formatted_date, open_price, high_price, low_price, close_price, volume, daily_change, percent_change))

    # Sort the stock data by date in descending order
    stock_data.sort(reverse=True)

    # Save the stock data to a CSV file
    with open(f'{stock_ticker}.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Daily Change', '% Change'])
        csvwriter.writerows(stock_data)

    # Print a message to indicate the CSV file has been saved
    print(f'Stock data for {stock_ticker} has been saved to {stock_ticker}.csv')

    # Print the most recent stock data
    latest_date, latest_open, latest_high, latest_low, latest_close, latest_volume, latest_daily_change, latest_percent_change = stock_data[0]
    print(f'Most recent data for {stock_ticker}:')
    print(f'Date: {latest_date}')
    print(f'Open: ${latest_open:,.2f}')
    print(f'Close: ${latest_close:,.2f}')
    print(f'Daily Change: ${latest_daily_change:,.2f}')
    print(f'% Change: {latest_percent_change:,.2f}%')

import requests
import csv
import numpy as np

from scipy.stats import iqr

from datetime import datetime

# Enter your Alpha Vantage API key here
api_key = 'R9RDVNKFONRCSA6D'

# List of stock tickers
stock_tickers = ['LMT', 'NOC']

for stock_ticker in stock_tickers:
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
            close_price = float(data['Time Series (Daily)'][date]['4. close'])
            stock_data.append((formatted_date, close_price))

        # Sort the stock data by date in ascending order
        stock_data.sort(key=lambda x: x[0])

        # Compute the log returns
        log_returns = []
        for i in range(1, len(stock_data)):
            previous_close = stock_data[i-1][1]
            current_close = stock_data[i][1]
            log_return = np.log(current_close) - np.log(previous_close)
            log_returns.append((stock_data[i][0], log_return))

        # Save the log returns to a CSV file
        with open(f'{stock_ticker}_log_returns.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date', 'Log Return'])
            csvwriter.writerows(log_returns)

        # Print a message to indicate the CSV file has been saved
        print(f'Log returns for {stock_ticker} has been saved to {stock_ticker}_log_returns.csv')

        # Print the most recent log return
        latest_date, latest_log_return = log_returns[-1]
        print(f'Most recent log return for {stock_ticker}:')
        print(f'Date: {latest_date}')
        print(f'Log Return: {latest_log_return:.2f}')
        
        # Convert log returns to a numpy array for easier calculations
        log_returns_arr = np.array([x[1] for x in log_returns])

        # Compute the minimum
        min_return = np.min(log_returns_arr)
        print(f'Minimum log return for {stock_ticker}: {min_return:.2f}')

        # Compute the maximum
        max_return = np.max(log_returns_arr)
        print(f'Maximum log return for {stock_ticker}: {max_return:.2f}')

        # Compute the mean (average)
        mean_return = np.mean(log_returns_arr)
        print(f'Mean log return for {stock_ticker}: {mean_return:.2f}')

        # Compute the 1st quartile (25th percentile)
        q1_return = np.quantile(log_returns_arr, 0.25)
        print(f'1st quartile log return for {stock_ticker}: {q1_return:.2f}')

        # Compute the 3rd quartile (75th percentile)
        q3_return = np.quantile(log_returns_arr, 0.75)
        print(f'3rd quartile log return for {stock_ticker}: {q3_return:.2f}')

        # Compute the interquartile range (IQR)
        iqr_return = iqr(log_returns_arr)
        print(f'IQR of log return for {stock_ticker}: {iqr_return:.2f}')
                
    

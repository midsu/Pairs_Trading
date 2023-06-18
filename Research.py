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
                
    
import requests
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import math
import numpy as np

def retrieve_stock_data(stock_ticker1, stock_ticker2):
    # Enter your Alpha Vantage API key here
    api_key = 'R9RDVNKFONRCSA6D'

    stock_tickers = [stock_ticker1, stock_ticker2]

    plt.figure(figsize=(10, 6))  # Create a larger figure size for better visualization

    closing_prices1 = []
    closing_prices2 = []

    for stock_ticker in stock_tickers:
        # Make a request to the Alpha Vantage API to retrieve the stock data
        response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock_ticker}&apikey={api_key}')

        # Parse the response data as JSON
        data = response.json()

        # Check if the API returned an error message
        if 'Error Message' in data:
            print(data['Error Message'])
        else:
            # Extract the closing prices for the last 120 days
            dates = sorted(data['Time Series (Daily)'].keys(), reverse=True)
            closing_prices = []
            for i, date in enumerate(dates):
                if i >= 120:
                    break
                close_price = float(data['Time Series (Daily)'][date]['4. close'])
                closing_prices.append(close_price)

            # Calculate the mean of the closing prices
            mean = np.mean(closing_prices)

            # Perform the subsequent calculations
            deviations = [(price - mean) for price in closing_prices]
            squared_deviations = [(deviation ** 2) for deviation in deviations]
            sum_squared_deviations = sum(squared_deviations)
            average_squared_deviation = sum_squared_deviations / (len(closing_prices) - 1)
            square_root_avg_squared_deviation = math.sqrt(average_squared_deviation)

            # Calculate the quartiles and interquartile range
            q1 = np.percentile(closing_prices, 25)
            q2 = np.percentile(closing_prices, 50)
            q3 = np.percentile(closing_prices, 75)
            iqr = q3 - q1

            # Print the results
            print(f"Mean of {stock_ticker} closing prices: {mean}")
            print(f"Sum of squared deviations from the mean (SS): {sum_squared_deviations}")
            print(f"Average squared deviation from the mean: {average_squared_deviation}")
            print(f"Square root of average squared deviation: {square_root_avg_squared_deviation}")
            print(f"Q1: {q1}")
            print(f"Q2 (Median): {q2}")
            print(f"Q3: {q3}")
            print(f"Interquartile Range (IQR): {iqr}\n")

            # Store the closing prices for each stock
            if stock_ticker == stock_ticker1:
                closing_prices1 = closing_prices
                plt.plot(closing_prices, color='blue', label=stock_ticker1)
            else:
                closing_prices2 = closing_prices
                plt.plot(closing_prices, color='red', label=stock_ticker2)

    # Set the plot title and labels
    plt.title('Closing Prices')
    plt.xlabel('Days')
    plt.ylabel('Price')

    # Add a legend
    plt.legend()

    # Show the plot
    plt.show()

    # Calculate the log returns
    log_returns1 = np.diff(np.log(closing_prices1))
    log_returns2 = np.diff(np.log(closing_prices2))

    # Plot the log returns
    plt.figure(figsize=(10, 6))
    plt.plot(log_returns1, color='blue', label=stock_ticker1)
    plt.plot(log_returns2, color='red', label=stock_ticker2)
    plt.title('Log Returns')
    plt.xlabel('Days')
    plt.ylabel('Log Return')
    plt.legend()
    plt.show()

    # Plot the quartiles and interquartile range for each stock
    plt.figure(figsize=(10, 6))
    plt.boxplot([closing_prices1, closing_prices2], labels=[stock_ticker1, stock_ticker2])
    plt.title('Quartiles and Interquartile Range')
    plt.xlabel('Stock Ticker')
    plt.ylabel('Closing Price')
    plt.show()

    # Calculate the correlation
    correlation = np.corrcoef(log_returns1, log_returns2)[0, 1]
    print(f"Correlation between {stock_ticker1} and {stock_ticker2}: {correlation}")

# Prompt the user to enter two stock tickers
stock_ticker1 = input('Enter the first stock ticker (e.g. AAPL): ')
stock_ticker2 = input('Enter the second stock ticker (e.g. GOOGL): ')

# Call the function to retrieve and plot the stock data
retrieve_stock_data(stock_ticker1, stock_ticker2)

import requests
import matplotlib.pyplot as plt
import math
import numpy as np
import statsmodels.api as sm

# Global variable
api_key = "Enter your api key here"

# Function to get the stock data from API
def get_stock_data(stock_ticker):
    response = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock_ticker}&apikey={api_key}')
    data = response.json()
    return data

# Function to extract the closing prices from the stock data
def extract_closing_prices(data):
    dates = sorted(data['Time Series (Daily)'].keys(), reverse=True)
    closing_prices = []
    for i, date in enumerate(dates):
        if i >= 120:
            break
        close_price = float(data['Time Series (Daily)'][date]['4. close'])
        closing_prices.append(close_price)
    return closing_prices

# Function to calculate and print statistics
def calc_statistics(closing_prices, stock_ticker):
    mean = np.mean(closing_prices)
    deviations = [(price - mean) for price in closing_prices]
    squared_deviations = [(deviation ** 2) for deviation in deviations]
    sum_squared_deviations = sum(squared_deviations)
    average_squared_deviation = sum_squared_deviations / (len(closing_prices) - 1)
    square_root_avg_squared_deviation = math.sqrt(average_squared_deviation)
    q1 = np.percentile(closing_prices, 25)
    q2 = np.percentile(closing_prices, 50)
    q3 = np.percentile(closing_prices, 75)
    iqr = q3 - q1

    print(f"Mean of {stock_ticker} closing prices: {mean}")
    print(f"Sum of squared deviations from the mean (SS): {sum_squared_deviations}")
    print(f"Average squared deviation from the mean: {average_squared_deviation}")
    print(f"Square root of average squared deviation: {square_root_avg_squared_deviation}")
    print(f"Q1: {q1}")
    print(f"Q2 (Median): {q2}")
    print(f"Q3: {q3}")
    print(f"Interquartile Range (IQR): {iqr}\n")

    return closing_prices

# Function to plot the closing prices of both stocks
def plot_prices(closing_prices1, closing_prices2, stock_ticker1, stock_ticker2):
    plt.figure(figsize=(10, 6))
    plt.plot(closing_prices1, color='blue', label=stock_ticker1)
    plt.plot(closing_prices2, color='red', label=stock_ticker2)
    plt.title('Closing Prices')
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Function to perform cointegration test and print result
def cointegration_test(log_returns1, log_returns2):
    residuals = log_returns2 - log_returns1
    adf_result = sm.tsa.stattools.adfuller(residuals)
    p_value = adf_result[1]
    is_cointegrated = p_value < 0.05
    print("The stocks are cointegrated.") if is_cointegrated else print("The stocks are not cointegrated.")
    return residuals

# Function to plot the residuals of cointegration test
def plot_residuals(residuals):
    plt.figure(figsize=(10, 6))
    plt.plot(residuals, color='green', label='Residuals')
    plt.axhline(0, color='black', linestyle='--')
    plt.title('Engle-Granger Residuals')
    plt.xlabel('Days')
    plt.ylabel('Residual')
    plt.legend()
    plt.show()

# Function to calculate and print the correlation between log returns of both stocks
def calc_corr(log_returns1, log_returns2, stock_ticker1, stock_ticker2):
    correlation = np.corrcoef(log_returns1, log_returns2)[0, 1]
    print(f"Correlation between {stock_ticker1} and {stock_ticker2}: {correlation}")

# User inputs for two stock tickers
stock_ticker1 = input('Enter the first stock ticker (e.g. AAPL): ')
stock_ticker2 = input('Enter the second stock ticker (e.g. GOOGL): ')

# Get stock data
data1 = get_stock_data(stock_ticker1)
data2 = get_stock_data(stock_ticker2)

# Extract closing prices
closing_prices1 = extract_closing_prices(data1)
closing_prices2 = extract_closing_prices(data2)

# Calculate and print statistics
closing_prices1 = calc_statistics(closing_prices1, stock_ticker1)
closing_prices2 = calc_statistics(closing_prices2, stock_ticker2)

# Plot closing prices
plot_prices(closing_prices1, closing_prices2, stock_ticker1, stock_ticker2)

# Calculate log returns
log_returns1 = np.diff(np.log(closing_prices1))
log_returns2 = np.diff(np.log(closing_prices2))

# Perform cointegration test ( long term prediction )
residuals = cointegration_test(log_returns1, log_returns2)

# Plot residuals
plot_residuals(residuals)

# Calculate and print correlation ( short term prediction )
calc_corr(log_returns1, log_returns2, stock_ticker1, stock_ticker2)

from datetime import datetime
import os
import pandas as pd
import yfinance as yf

DATA_DIR = "data"  # Directory to store the fetched data
STOCK_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # List of stock tickers to fetch data for
CRYPTO_SYMBOLS = ["BTC-USD", "ETH-USD", "LTC-USD"]  # List of cryptocurrency symbols to fetch data for
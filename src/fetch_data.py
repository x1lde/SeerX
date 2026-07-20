from datetime import datetime, timedelta
import os
import pandas as pd
import yfinance as yf

DATA_DIR = "data"  # Directory to store the fetched data
STOCK_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # List of stock tickers to fetch data for
CRYPTO_SYMBOLS = ["BTC-USD", "ETH-USD", "LTC-USD"]  # List of cryptocurrency symbols to fetch data for

def fetch_stock(ticker:str) -> pd.DataFrame: # Fetch stock data for a given ticker symbol
    df = yf.Ticker(ticker).history(period="5d").reset_index() # Fetch the last 5 days of stock data for the given ticker
    df["Date"] = pd.to_datetime(df["Date"]).dt.date # Convert the Date column to date format
    df["Symbol"] = ticker # Add the ticker symbol to the DataFrame
    return df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]] # Return only the relevant columns

def fetch_crypto(symbol:str) -> pd.DataFrame: # Fetch cryptocurrency data for a given symbol
    from alpaca.data.historical import CryptoHistoricalDataClient # Import the Alpaca CryptoHistoricalDataClient
    from alpaca.data.requests import CryptoBarsRequest # Import the CryptoBarsRequest class
    from alpaca.data.timeframe import TimeFrame # Import the TimeFrame class

    client = CryptoHistoricalDataClient() # Create an instance of the CryptoHistoricalDataClient
    request = CryptoBarsRequest(
        symbol_or_symbols=symbol, # Specify the cryptocurrency symbol to fetch data for
        timeframe=TimeFrame.Day, # Set the timeframe to daily data
        start=datetime.utcnow() - timedelta(days=5), # Set the start date to 5 days ago
    )
    df  = client.get_crypto_bars(request).df.reset_index() # Fetch the cryptocurrency data and reset the index
    df = df.rename(columns={
        "timestamp": "Date", # Rename the timestamp column to Date
        "symbol": "Symbol", # Rename the symbol column to Symbol
        "open": "Open", # Rename the open column to Open
        "high": "High", # Rename the high column to High
        "low": "Low", # Rename the low column to Low
        "close": "Close", # Rename the close column to Close
        "volume": "Volume"  # Rename the volume column to Volume
    })
    df["Date"] = pd.to_datetime(df["Date"]).dt.date # Convert the Date column to date format
    return df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]] # Return only the relevant columns

def save_to_csv(df: pd.DataFrame, path: str) -> None: # Save the DataFrame to a CSV file
    os.makedirs(os.path.dirname(path), exist_ok=True) # Create the directory if it doesn't exist
    if os.path.exists(path): # Check if the file already exists
        existing = pd.read_csv(path) # Read the existing CSV file
        existing["Date"] = pd.to_datetime(existing["Date"]).dt.date # Convert the Date column to date format
        combined = pd.concat([existing, df]).drop_duplicates(subset=["Date", "Symbol"]) # Combine the existing and new data, dropping duplicates based on Date and Symbol
    else:
        combined = df # If the file doesn't exist, use the new data as is
    combined.sort_values("Date").to_csv(path, index=False) # Sort the combined data by Date and save it to the CSV file without the index

def main():
    for ticker in STOCK_TICKERS: # Loop through each stock ticker
        try:
            df = fetch_stock(ticker) # Fetch the stock data for the ticker
            save_to_csv(df, f"{DATA_DIR}/stocks/{ticker}.csv") # Save the data to a CSV file
            print(f"Fetched and saved data for stock: {ticker}") # Print a message indicating that the data has been fetched and saved
        except Exception as e:
            print(f"Error fetching data for stock {ticker}: {e}")

    for symbol in CRYPTO_SYMBOLS: # Loop through each cryptocurrency symbol
        try:
            df = fetch_crypto(symbol) # Fetch the cryptocurrency data for the symbol
            safe_name = symbol.replace("/", "-") # Replace any slashes in the symbol with hyphens to create a safe filename
            save_to_csv(df, f"{DATA_DIR}/crypto/{safe_name}.csv") # Save the data to a CSV file
        except Exception as e: # Handle any exceptions that occur during the fetching or saving process
            print(f"Error fetching data for cryptocurrency {symbol}: {e}") # Print a message indicating that there was an error fetching data for the cryptocurrency

if __name__ == "__main__": # Check if the script is being run directly (not imported as a module)
    main() # Call the main function to execute the data fetching and saving process
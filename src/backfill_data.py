import pandas as pd
import yfinance as yf

from fetch_data import STOCK_TICKERS, save_to_csv, DATA_DIR

def backfill_stock(ticker: str, period='2y') -> pd.DataFrame: # Fetch stock data for a given ticker symbol over a specified period
    df = yf.Ticker(ticker).history(period=period).reset_index()  # Fetch the last 2 years of stock data for the given ticker
    df["Date"] = pd.to_datetime(df["Date"]).dt.date  # Convert the Date column to date format
    df["Symbol"] = ticker  # Add the ticker symbol to the DataFrame
    return df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]]  # Return only the relevant columns

def main():
    for ticker in STOCK_TICKERS:  # Loop through each stock ticker
        try:
            df = backfill_stock(ticker)  # Fetch the stock data for the ticker
            save_to_csv(df, f"{DATA_DIR}/stocks/{ticker}.csv")  # Save the data to a CSV file
            print(f"Backfilled and saved data for stock: {ticker}")  # Print a message indicating that the data has been backfilled and saved
        except Exception as e:
            print(f"Error backfilling data for stock {ticker}: {e}")

if __name__ == "__main__":
    main()  # Call the main function to execute the backfilling process

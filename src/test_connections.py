import os
from dotenv import load_dotenv

load_dotenv()

def test_yfinance_connection():
    import yfinance as yf

    ticker = yf.Ticker("AAPL") # create a Ticker object for Apple Inc.
    hist = ticker.history(period="5d") # fetch the historical data for the last 5 days
    if hist.empty:
        raise RuntimeError("Failed to fetch historical data from yfinance.") # if the history is empty, raise an error
    print(f"yfinance pulled {len(hist)} rows of historical data.") # print the number of rows pulled
    print(hist.tail(1)[['Close', 'Open', 'Volume']]) # print the last row of the historical data with Close, Open, and Volume columns

def test_alpaca_connection():
    from alpaca_trade_api.rest import TradingClient

    api_key = os.getenv("ALPACA_API_KEY") # get the API key from the environment variables
    secret_key = os.getenv("ALPACA_SECRET_KEY") # get the secret key from the environment variables

    if not api_key or api_key == "your_key_here":
        raise RuntimeError("ALPACA_API_KEY and ALPACA_SECRET_KEY must be set in the environment variables.") # if the API keys are not set, raise an error
    
    if not secret_key or secret_key == "your_secret_here":
        raise RuntimeError("ALPACA_API_KEY and ALPACA_SECRET_KEY must be set in the environment variables.") # if the API keys are not set, raise an error

    client = TradingClient(api_key, secret_key, paper=True) # create a TradingClient object with the API keys and set paper trading to True
    account = client.get_account() # fetch the account information
    print("Successfully connected to paper account.") # print a success message
    print(f"Alpaca account status: {account.status}") # print the account status

if __name__ == "__main__":
    print("Testing yfinance connection...")

    try:
        test_yfinance_connection() # test the yfinance connection
    except Exception as e:
        print(f"yfinance connection test failed: {e}") # if the test fails, print the error message
    
    print()

    try:
        test_alpaca_connection() # test the Alpaca connection
    except Exception as e:
        print(f"Alpaca connection test failed: {e}") # if the test fails, print the error message

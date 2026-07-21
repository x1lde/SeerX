import glob
import os
from datetime import date

import joblib
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

from features import FEATURES, add_features

load_dotenv()  # Load environment variables from .env file

DATA_DIR = "data"  # Directory where the fetched data is stored
MODEL_PATH = "models/baseline_model.joblib"  # Path to save the trained model
TRADE_QTY = 1  # Number of shares to trade per signal

def load_latest_rows(): # Load the latest rows of stock data from CSV files in the data directory
    frames = [pd.read_csv(p, parse_dates=["Date"]) for p in glob.glob(f"{DATA_DIR}/stocks/*.csv")]  # Load all stock CSV files into DataFrames
    df = pd.concat(frames, ignore_index=True)  # Concatenate all DataFrames into a single DataFrame
    df = add_features(df) # Add features to the DataFrame for model training
    df = df.dropna(subset=FEATURES + ["target"]) # Drop rows with NaN values in the specified features and target column
    return df.sort_values("Date").groupby("Symbol").tail(1)  # Return the latest row for each symbol

def get_held_qty(trading_client, symbol) -> float: # Get the quantity of shares currently held for a given symbol
    try:
        position = trading_client.get_open_position(symbol)  # Get the current position for the given symbol
        return float(position.qty)  # Return the quantity of shares held
    except Exception:
        return 0.0  # If there is an error (e.g., no position), return 0.0
    
def place_order(trading_client, symbol, side, qty): # Place a market order to buy or sell a specified quantity of shares for a given symbol
    from alpaca.trading.requests import MarketOrderRequest # Import the MarketOrderRequest class from the Alpaca trading requests module
    from alpaca.trading.enums import OrderSide, TimeInForce # Import the OrderSide and TimeInForce enums from the Alpaca trading enums module

    order_data = MarketOrderRequest( # Create a market order request with the specified parameters
        symbol=symbol, # The stock symbol to trade
        qty=qty, # The quantity of shares to trade (set to the global TRADE_QTY variable)
        side=OrderSide.BUY if side == "buy" else OrderSide.SELL, # Determine the order side (buy or sell) based on the input parameter
        time_in_force=TimeInForce.DAY # Set the time in force for the order to "day" (the order will be valid for the trading day)
    )
    return trading_client.submit_order(order_data) # Submit the order request to the Alpaca trading client

def main():
    from alpaca.trading.client import TradingClient # Import the TradingClient class from the Alpaca trading client module
    trading_client = TradingClient(
        os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True
        ) # Initialize the Alpaca trading client with API credentials from environment variables
    supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")) # Initialize the Supabase client with URL and key from environment variables

    model = joblib.load(MODEL_PATH) # Load the trained model from the specified path
    today = date.today().isoformat()
    latest = load_latest_rows() # Load the latest rows of stock data

    for _, row in latest.iterrows(): # Iterate over each row in the latest stock data
        symbol = row["Symbol"] # Get the stock symbol from the current row
        pred = model.predict(pd.DataFrame([row[FEATURES]], columns=FEATURES))[0] # Make a prediction using the trained model for the current row's features
        direction = "buy" if pred == 1 else "sell" # Determine the trade direction based on the prediction

        print(f"{today} - {symbol}: Predicted direction: {direction}") # Print the predicted direction for the current symbol

        supabase.table("predictions").insert(
            {
                "date": today, # Insert the current date into the predictions table
                "symbol": symbol, # Insert the stock symbol into the predictions table
                "predicted_direction": direction, # Insert the predicted direction into the predictions table
            }
        ).execute() # Execute the insert operation

        held_qty = get_held_qty(trading_client, symbol) # Get the quantity of shares currently held for the current symbol
        side = None
        if direction == "buy" and held_qty == 0: # If the predicted direction is "buy" and no shares are currently held
            side = "buy" # Set the order side to "buy"
        elif direction == "sell" and held_qty > 0: # If the predicted direction is "sell" and shares are currently held
            side = "sell" # Set the order side to "sell"

        if side is None:
            print(f"No action needed for {symbol}.") # Print a message indicating that no action is needed for the current symbol
            continue

        try:
            place_order(trading_client, symbol, side, TRADE_QTY) # Attempt to place a market order for the current symbol with the determined side and quantity
            print(f"Placed {side} order for {symbol}.") # Print a message indicating that the order has been placed
            supabase.table("trades").insert(
                {
                    "date": today, # Insert the current date into the orders table
                    "symbol": symbol, # Insert the stock symbol into the orders table
                    "side": side, # Insert the order side into the orders table
                    "qty": TRADE_QTY, # Insert the quantity of shares traded into the orders table
                }
            ).execute() # Execute the insert operation
        except Exception as e:
            print(f"Error placing order for {symbol}: {e}") # Print an error message if there is an exception while placing the order   

if __name__ == "__main__":
    main() # Call the main function to execute the trading engine
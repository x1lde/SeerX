FEATURES = ["return_1d", "return_5d", "ma_5d", "ma_10", "volatility_5d", "price_vs_5ma"] # Features for the model

def add_features(df): # Add features to the DataFrame for model training
    df = df.sort_values("symbol", "Date").copy() # Sort the DataFrame by symbol and date, and create a copy to avoid modifying the original DataFrame

    df["return_1d"] = df.groupby("symbol")["Close"].pct_change(1) # Calculate the 1-day return of the closing price
    df["return_5d"] = df.groupby("symbol")["Close"].pct_change(5) # Calculate the 5-day return of the closing price
    df["ma_5d"] = df.groupby("symbol")["Close"].transform(lambda s: s.rolling(window=5).mean()) # Calculate the 5-day moving average of the closing price
    df["ma_10"] = df.groupby("symbol")["Close"].transform(lambda s: s.rolling(window=10).mean()) # Calculate the 10-day moving average of the closing price
    df["volatility_5d"] = df.groupby("symbol")["return_1d"].transform(lambda s: s.rolling(window=5).std()) # Calculate the 5-day rolling standard deviation of daily returns
    df["price_vs_5ma"] = df["Close"] / df["ma_5d"] - 1 # Calculate the price relative to the 5-day moving average

    # Did the price go up?
    df["next_close"] = df.groupby("symbol")["Close"].shift(-1) # Shift the closing price to get the next day's closing price
    df["target"] = (df["next_close"] > df["Close"]).astype(int) # Create a binary target variable indicating if the next day's closing price is higher than today's

    return df.dropna() # Drop rows with NaN values that may have been introduced by the feature calculations
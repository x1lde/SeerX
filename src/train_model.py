import glob
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from features import FEATURES, add_features

DATA_DIR = "data"  # Directory where the fetched data is stored
MODEL_DIR = "models"  # Directory to save the trained model

def load_all_stock_data() -> pd.DataFrame: # Load all stock data from CSV files in the data directory
    frames = [pd.read_csv(p, parse_dates=["Date"]) for p in glob.glob(f"{DATA_DIR}/stocks/*.csv")]  # Load all stock CSV files into DataFrames
    return pd.concat(frames, ignore_index=True)  # Concatenate all DataFrames into a single DataFrame

def add_features(df: pd.DataFrame) -> pd.DataFrame: # Add features to the DataFrame for model training
    # Example feature addition (replace with actual feature engineering logic)
    df["return_1d"] = df.groupby("Symbol")["Close"].pct_change(1) # Calculate the 1-day return of the closing price
    df["return_5d"] = df.groupby("Symbol")["Close"].pct_change(5) # Calculate the 5-day return of the closing price
    df["ma_5d"] = df.groupby("Symbol")["Close"].transform(lambda s: s.rolling(window=5).mean()) # Calculate the 5-day moving average of the closing price
    df["ma_10"] = df.groupby("Symbol")["Close"].transform(lambda s: s.rolling(window=10).mean()) # Calculate the 10-day moving average of the closing price
    df["volatility_5d"] = df.groupby("Symbol")["return_1d"].transform(lambda s: s.rolling(window=5).std()) # Calculate the 5-day rolling standard deviation of daily returns
    df["price_vs_5ma"] = df["Close"] / df["ma_5d"] - 1 # Calculate the price relative to the 5-day moving average

    # Did the price go up?
    df["next_close"] = df.groupby("Symbol")["Close"].shift(-1) # Shift the closing price to get the next day's closing price
    df["target"] = (df["next_close"] > df["Close"]).astype(int) # Create a binary target variable indicating if the next day's closing price is higher than today's

    return df.dropna()

def train_and_evaluate(df: pd.DataFrame):
    df = df.sort_values("Date") # Sort the DataFrame by date
    split_index = int(len(df) * 0.8) # Split the data into training and testing sets (80% train, 20% test)
    train, test = df.iloc[:split_index], df.iloc[split_index:] # Training and testing sets

    X_train, y_train = train[FEATURES], train["target"] # Features and target for training
    X_test, y_test = test[FEATURES], test["target"] # Features and target for testing

    model = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42) # Initialize the Random Forest Classifier
    model.fit(X_train, y_train) # Fit the model to the training data

    preds = model.predict(X_test) # Make predictions on the test set
    accuracy = accuracy_score(y_test, preds) # Calculate the accuracy of the model
    naive_baseline = (y_test == 1).mean() # Calculate the naive baseline accuracy (proportion of positive cases)

    print(f"Model Accuracy: {accuracy:.4f}") # Print the model accuracy
    print(f"Naive Baseline Accuracy: {naive_baseline:.4f}") # Print the naive baseline accuracy
    print()
    print(classification_report(y_test, preds)) # Print the classification report

    return model # Return the trained model

def main():
    print("Loading stock data...") # Print a message indicating that stock data is being loaded
    df = load_all_stock_data() # Load all stock data
    print(f"Loaded {len(df)} rows of stock data.") # Print the number of rows loaded

    print("Adding features...") # Print a message indicating that features are being added
    df = add_features(df).dropna(subset=FEATURES + ["target"]) # Add features to the DataFrame and drop rows with NaN values in the specified features and target column
    print(f"Data after feature engineering has {len(df)} rows.") # Print the number of rows after feature engineering

    print("Training and evaluating model...") # Print a message indicating that the model is being trained and evaluated
    model = train_and_evaluate(df) # Train and evaluate the model

    os.makedirs(MODEL_DIR, exist_ok=True) # Create the model directory if it doesn't exist
    model_path = f"{MODEL_DIR}/baseline_model.joblib" # Define the path to save the trained model
    joblib.dump(model, model_path) # Save the trained model to a file
    print(f"Trained model saved to {model_path}") # Print a message indicating that the trained model has been saved

if __name__ == "__main__":
    main() # Call the main function to execute the training process
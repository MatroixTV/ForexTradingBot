import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def train_trade_decision_model(input_file, output_model):
    """
    Trains a classification model to predict trade signals.
    """
    # Load the training data
    df = pd.read_csv(input_file)
    features = ['RSI', 'MACD', 'MACD_Signal', 'RTD_Trend', 'RSI_Squared', 'MACD_Signal_Diff']
    X = df[features]
    y = df['Target']

    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Validate the model
    y_val_pred = model.predict(X_val)
    print("Validation Classification Report:")
    print(classification_report(y_val, y_val_pred))

    # Save the model
    joblib.dump(model, output_model)
    print(f"Model saved to {output_model}")

if __name__ == "__main__":
    train_trade_decision_model("training_dataset.csv", "trade_decision_model.pkl")

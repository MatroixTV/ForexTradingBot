import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def train_model():
    # Load dataset
    df = pd.read_csv('training_dataset.csv')

    # Split into features and target
    X = df.drop(columns=['target'])
    y = df['target']

    # Split into training and test sets
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, 'trade_decision_model.pkl')
    print("Model saved as trade_decision_model.pkl")

if __name__ == "__main__":
    train_model()

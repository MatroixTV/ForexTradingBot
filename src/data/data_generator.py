import pandas as pd
from sklearn.model_selection import train_test_split


def generate_dataset(df):
    """
    Generate dataset for supervised learning.
    """
    # Include indicators as features
    features = ['RSI', 'MACD', 'MACD_Signal', 'RTD_Trend']
    df = df[features + ['Close']]

    # Create lagged features
    for feature in features:
        for lag in range(1, 4):
            df[f'{feature}_lag_{lag}'] = df[feature].shift(lag)

    # Define target (1: profitable trade, 0: loss)
    df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # Drop rows with NaN values (due to lagging)
    df.dropna(inplace=True)

    # Save dataset
    df.to_csv('training_dataset.csv', index=False)
    print("Dataset saved to training_dataset.csv")
    return df


if __name__ == "__main__":
    from src.indicators.indicators_setup import calculate_indicators

    df = pd.read_csv('C:/Users/ismac/PycharmProjects/forex_trading_bot/data/EURUSD.csv')
    df = calculate_indicators(df)
    generate_dataset(df)

import pandas as pd

def generate_training_data(input_file, output_file):
    """
    Generates a training dataset with features and targets for supervised ML.
    """
    # Load the processed data
    df = pd.read_csv(input_file)

    # Feature engineering
    df['RSI_Squared'] = df['RSI'] ** 2
    df['MACD_Signal_Diff'] = df['MACD'] - df['MACD_Signal']

    # Assign target based on trading conditions
    df['Target'] = 0  # Default: No trade
    df.loc[(df['RSI'] < 30) & (df['RTD_Trend'] > 0), 'Target'] = 1  # Buy
    df.loc[(df['RSI'] > 70) & (df['RTD_Trend'] < 0), 'Target'] = -1  # Sell

    # Save the training dataset
    features = ['RSI', 'MACD', 'MACD_Signal', 'RTD_Trend', 'RSI_Squared', 'MACD_Signal_Diff']
    df[features + ['Target']].to_csv(output_file, index=False)
    print(f"Training dataset saved to {output_file}")

if __name__ == "__main__":
    generate_training_data("processed_data.csv", "training_dataset.csv")

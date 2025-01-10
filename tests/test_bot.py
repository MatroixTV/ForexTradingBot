import pandas as pd
from src.indicators.indicators_setup import add_indicators

# Create a mock dataframe with required columns
data = {
    "Close": [1.1234, 1.1256, 1.1245, 1.1267, 1.1250, 1.1278, 1.1285, 1.1290, 1.1280, 1.1265,
              1.1275, 1.1288, 1.1295, 1.1302, 1.1310, 1.1320, 1.1330, 1.1340, 1.1350, 1.1360],
    "High": [1.1250, 1.1260, 1.1270, 1.1280, 1.1290, 1.1300, 1.1305, 1.1307, 1.1299, 1.1288,
             1.1298, 1.1305, 1.1312, 1.1318, 1.1325, 1.1335, 1.1345, 1.1355, 1.1365, 1.1375],
    "Low": [1.1220, 1.1230, 1.1240, 1.1250, 1.1240, 1.1255, 1.1260, 1.1265, 1.1260, 1.1250,
            1.1258, 1.1265, 1.1272, 1.1278, 1.1285, 1.1295, 1.1305, 1.1315, 1.1325, 1.1335],
}
df = pd.DataFrame(data)


# Apply indicators
df_with_indicators = add_indicators(df)

print(df_with_indicators)

assert not df_with_indicators["RSI"].isnull().any(), "RSI is not being calculated."
assert not df_with_indicators["MACD"].isnull().any(), "MACD is not being calculated."
assert not df_with_indicators["BB_Upper"].isnull().any(), "Bollinger Bands are not being calculated."
assert not df_with_indicators["XMODE"].isnull().any(), "XMODE is not being calculated."
assert not df_with_indicators["BB_Upper"].isnull().all(), "Bollinger Bands are not being calculated."
assert not df_with_indicators["BB_Lower"].isnull().all(), "Bollinger Bands are not being calculated."

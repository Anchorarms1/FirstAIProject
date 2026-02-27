import pandas_ta as ta
import pandas as pd

class TechnicalAnalysisService:
    @staticmethod
    def calculate_indicators(historical_data):
        df = pd.DataFrame(historical_data)
        df['close_price'] = df['close_price'].astype(float)
        df['RSI'] = ta.rsi(df['close_price'], length=14)
        macd = ta.macd(df['close_price'])
        df = pd.concat([df, macd], axis=1)
        df['SMA_20'] = ta.sma(df['close_price'], length=20)
        df['SMA_50'] = ta.sma(df['close_price'], length=50)
        return df

    @staticmethod
    def get_latest_signals(df):
        latest = df.iloc[-1]
        return {
            "price": latest['close_price'],
            "rsi": latest.get('RSI'),
            "macd": latest.get('MACD_12_26_9'),
            "macd_signal": latest.get('MACDs_12_26_9'),
            "sma_20": latest.get('SMA_20'),
            "sma_50": latest.get('SMA_50')
        }

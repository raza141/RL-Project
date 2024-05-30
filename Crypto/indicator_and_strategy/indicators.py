import talib
import pandas as pd
from dataclasses import dataclass

@dataclass
class Indicator:
    dataset: pd.DataFrame
    window: int = 14

    def rsi(self):
        """Calculate the Relative Strength Index (RSI) using the talib library."""
        try:
            return talib.RSI(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating RSI: {e}")
            return pd.Series(dtype='float64')

    def macd(self):
        """Calculate the Moving Average Convergence Divergence (MACD) using the talib library."""
        try:
            _, _, macd_hist = talib.MACD(self.dataset.close)
            return macd_hist
        except Exception as e:
            print(f"Error calculating MACD: {e}")
            return pd.Series(dtype='float64')

    def ema(self):
        """Calculate the Exponential Moving Average (EMA) using the talib library."""
        try:
            return talib.EMA(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating EMA: {e}")
            return pd.Series(dtype='float64')

    def sma(self):
        """Calculate the Simple Moving Average (SMA) using the talib library."""
        try:
            return talib.SMA(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating SMA: {e}")
            return pd.Series(dtype='float64')

    def bollinger_bands(self):
        """Calculate the Bollinger Bands using the talib library.
        
        Returns:
            pd.DataFrame: DataFrame containing the Bollinger Bands(upper, middle, lower).
        """
        try:
            upper, middle, lower = talib.BBANDS(self.dataset.close, self.window)
            return pd.DataFrame({'Upper Band': upper, 'Middle Band': middle, 'Lower Band': lower})
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {e}")
            return pd.DataFrame()

    def adx(self):
        """Calculate the Average Directional Index (ADX) using the talib library.
        
        Returns:
            pd.Series: Series containing the ADX values.
        """
        try:
            return talib.ADX(self.dataset.high, self.dataset.low, self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating ADX: {e}")
            return pd.Series(dtype='float64')

    def cci(self):
        """Calculate the Commodity Channel Index (CCI) using the talib library."""
        try:
            return talib.CCI(self.dataset.high, self.dataset.low, self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating CCI: {e}")
            return pd.Series(dtype='float64')

    def atr(self):
        """Calculate the Average True Range (ATR) using the talib library.
        
        Returns:
            pd.Series: Series containing the ATR values.
        """
        try:
            return talib.ATR(self.dataset.high, self.dataset.low, self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating ATR: {e}")
            return pd.Series(dtype='float64')

    def roc(self):
        """Calculate the Rate of Change (ROC) using the talib library."""
        try:
            return talib.ROC(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating ROC: {e}")
            return pd.Series(dtype='float64')

    def stoch(self):
        """Calculate the Stochastic Oscillator using the talib library.
        
        Returns:
            pd.DataFrame: DataFrame containing the Stochastic Oscillator values(slowk, slowd).
        """
        try:
            slowk, slowd = talib.STOCH(self.dataset.high, self.dataset.low, self.dataset.close)
            return pd.DataFrame({'SlowK': slowk, 'SlowD': slowd})
        except Exception as e:
            print(f"Error calculating Stochastic Oscillator: {e}")
            return pd.DataFrame()

    def williams(self):
        """Calculate the Williams %R using the talib library."""
        try:
            return talib.WILLR(self.dataset.high, self.dataset.low, self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating Williams %R: {e}")
            return pd.Series(dtype='float64')

    def obv(self):
        """Calculate the On Balance Volume (OBV) using the talib library."""
        try:
            return talib.OBV(self.dataset.close, self.dataset.volume)
        except Exception as e:
            print(f"Error calculating OBV: {e}")
            return pd.Series(dtype='float64')

    def momentum(self):
        """Calculate the Momentum using the talib library."""
        try:
            return talib.MOM(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating Momentum: {e}")
            return pd.Series(dtype='float64')

    def donchian(self):
        """Calculate the Donchian Channel using the talib library."""
        try:
            return talib.DPO(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating Donchian Channel: {e}")
            return pd.Series(dtype='float64')

    def aroon(self):
        """Calculate the Aroon indicator using the talib library."""
        try:
            aroondown, aroonup = talib.AROON(self.dataset.high, self.dataset.low, self.window)
            return pd.DataFrame({'Aroon Down': aroondown, 'Aroon Up': aroonup})
        except Exception as e:
            print(f"Error calculating Aroon: {e}")
            return pd.DataFrame()

    def adix(self):
        """Calculate the Average Directional Index Rating (ADXR) using the talib library."""
        try:
            return talib.ADXR(self.dataset.high, self.dataset.low, self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating ADXR: {e}")
            return pd.Series(dtype='float64')

    def cmo(self):
        """Calculate the Chande Momentum Oscillator (CMO) using the talib library."""
        try:
            return talib.CMO(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating CMO: {e}")
            return pd.Series(dtype='float64')

    def trix(self):
        """Calculate the TRIX indicator using the talib library."""
        try:
            return talib.TRIX(self.dataset.close, self.window)
        except Exception as e:
            print(f"Error calculating TRIX: {e}")
            return pd.Series(dtype='float64')
        x
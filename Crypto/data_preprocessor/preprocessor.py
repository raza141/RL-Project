import pandas as pd
from dataclasses import dataclass

@dataclass
class DataPreprocessor:
    data: any 
    source: str = 'binance'
    """
    Initialize the DataPreprocessor with data and source type.
    
    :param data: The data to preprocess (list of lists, tuple, or pandas DataFrame).
    :param source: The source type ('generic', 'ccxt', 'yfinance').
    """
    
    def preprocess(self):
        """
        Preprocess the data into a pandas DataFrame.
        
        :return: A pandas DataFrame with the appropriate columns.
        """
        if isinstance(self.data, (list, tuple)):
            if isinstance(self.data[0], list) or isinstance(self.data[0], tuple):
                df = self._list_to_dataframe(self.data)
            else:
                raise ValueError("Unsupported list structure")
        elif isinstance(self.data, pd.DataFrame):
            df = self.data
        else:
            raise ValueError("Unsupported data type")
        
        # Adjust columns based on source
        df = self._adjust_columns(df)
        self.df = df  # Store the dataframe in the instance for later use
        return df

    def _list_to_dataframe(self, data):
        """
        Convert a list of lists or list of tuples into a pandas DataFrame.
        
        :param data: List of lists or list of tuples.
        :return: A pandas DataFrame.
        """
        if len(data[0]) == 6:
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        elif len(data[0]) == 7:
            columns = ['timestamp', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        else:
            raise ValueError("Unsupported data structure length")
        
        df = pd.DataFrame(data, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Adjust based on timestamp format
        return df

    def _adjust_columns(self, df):
        """
        Adjust the columns of the DataFrame based on the source.
        
        :param df: The pandas DataFrame to adjust.
        :return: The adjusted pandas DataFrame.
        """
        if self.source == 'ccxt':
            if 'adj_close' not in df.columns:
                df.insert(5, 'adj_close', df['close'])
            df.set_index('timestamp', inplace=True)
        elif self.source == 'yfinance':
            df.reset_index(inplace=True)
        else:
            df.set_index('timestamp', inplace=True)  # Default action for generic source
        return df

    def get_columns(self, *columns):
        """
        Get specific columns from the DataFrame.
        
        :param columns: Column names to extract.
        :return: A pandas DataFrame containing only the specified columns.
        """
        if not hasattr(self, 'df'):
            raise ValueError("Data has not been preprocessed yet. Call preprocess() first.")
        
        missing_columns = [col for col in columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"The following columns are not in the DataFrame: {missing_columns}")
        
        return self.df[list(columns)]



if __name__ == '__main__':
    df = pd.DataFrame({
        'timestamp': [1609459200000, 1609545600000],
        'open': [100, 200],
        'high': [110, 210],
        'low': [90, 190],
        'close': [105, 205],
        'volume': [10000, 20000]
    })
    # Preprocess data from ccxt
    preobj = DataPreprocessor(df, source='ccxt').preprocess()

    # Get specific columns for charting/manipulating
    ccxt_columns = preobj.get_columns('timestamp', 'close')
    print(ccxt_columns.head())
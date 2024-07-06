from abc import ABC, abstractmethod
import logging
import json
from pathlib import Path
import ccxt
import yfinance as yf
import pandas as pd

class DataFetcher(ABC):
    """
    This class is used to fetch data from different data sources(e.g. binance, yfinance).

    Args:
        config_file_path (Path): The path to the config file(config.json). If not provided, the current working directory is used.

    Attributes:
        config (dict): The loaded config file.

    Methods:
        fetch_data(self):
    """



    def __init__(self, config_file_path: Path = None):
        self.setup_logging()
        if config_file_path is None:
            self.config_file: Path = Path.cwd() / 'config.json' 
        else: 
            self.config_file = config_file_path
        self.config = self._load_config()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[logging.FileHandler("exchange_data_fetcher.log"),
                                      logging.StreamHandler()])
        self.logger = logging.getLogger()

    def _load_config(self):
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        return config

    def get_exception(self):
        return self.exception

    @abstractmethod
    def fetch_data(self):
        pass



class CcxtFetcher(DataFetcher):
    def __init__(self, exchange_id: str = 'binance', config_file_path: Path = None):
        super().__init__(config_file_path)
        self.exchange_id = exchange_id
        self.exchange = self.setup_exchange()

    def setup_exchange(self):
        try: 
            exchange_id = self.config[self.exchange_id].get('exchange', 'binance')
            api_key = self.config[self.exchange_id].get('api_key', "")
            secret_key = self.config[self.exchange_id].get('secret_key', "")
            exchange = getattr(ccxt, exchange_id)({
                'apiKey': api_key,
                'secret': secret_key,
            })
            self.logger.info(f"Initialized exchange: {exchange_id}")
            return exchange
        except Exception as e:
            self.logger.error(f"Failed to initialize exchange: {e}")
            self.exception = e
            return None

    def fetch_data(self):
        """
        Fetches OHLCV (Open, High, Low, Close, Volume) data for a given symbol, timeframe, and limit.

        Returns:
            pandas.DataFrame: A DataFrame containing the fetched OHLCV data, with columns 'date', 'open', 'high', 'low', 'close', 'volume', 'tic', and 'day'.
                             If an error occurs during the fetching process, returns None.

        Raises:
            ccxt.NetworkError: If a network error occurs while fetching the data.
            ccxt.ExchangeError: If an exchange error occurs while fetching the data.
            Exception: If any other error occurs during the fetching process.

        """
        symbol = self.config[self.exchange_id].get('symbol', 'BTC/USDT')
        timeframe = self.config[self.exchange_id].get('timeframe', '1m')
        limit = self.config[self.exchange_id].get('limit', 100)

        self.logger.info(f"Fetching OHLCV data for {symbol} with timeframe {timeframe} and limit {limit}")
        
        try:
            ohlcv_data = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            self.logger.info("Successfully fetched OHLCV data")
            df = pd.DataFrame(ohlcv_data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
            df.date = pd.to_datetime(df.date, unit='ms')
            df.insert(1, 'tic', symbol)
            df['day'] = df['date'].dt.dayofweek
            
            return df
        
        except ccxt.NetworkError as e:
            self.logger.error(f"Network error: {e}")
            self.exception = e

        except ccxt.ExchangeError as e:
            self.logger.error(f"Exchange error: {e}")
            self.exception = e

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            self.exception = e
            
        return None

class YFinanceFetcher(DataFetcher):
    def __init__(self, exchange_id: str = 'yfinance', config_file_path: Path = None):
        super().__init__(config_file_path)
        self.exchange_id = exchange_id

    def fetch_data(self):
        symbol = self.config[self.exchange_id].get('symbol', 'AAPL')
        start_date = self.config[self.exchange_id].get('start_date', '2020-01-01')
        end_date = self.config[self.exchange_id].get('end_date', '2021-01-01')

        self.logger.info(f"Fetching stock data for {symbol} from {start_date} to {end_date}")
        try:
            data = yf.download(symbol, start=start_date, end=end_date)
            self.logger.info("Successfully fetched stock data")
            return data
        except Exception as e:
            self.logger.error(f"An error occurred while fetching stock data: {e}")
            self.exception = e
            return None


class BinanceStreamer(DataFetcher):
    def __init__(self, config_file_path: Path = None):
        super().__init__(config_file_path)

    def fetch_data(self):
        pass


def data_fetcher_factory(source: str, config_file_path: Path = None):
    """
    Function that creates and returns a data fetcher based on the input source and configuration file path.

    Parameters:
    source (str): The source of the data fetcher(e.g. binance, yfinance).
    config_file_path (Path, optional): The path to the configuration file. Defaults to None.

    Returns:
    DataFetcher: An instance of the appropriate data fetcher based on the input source and configuration file path.
    Raises:
    ValueError: If the data source is unknown.
    """
    if source == 'yfinance':
        return YFinanceFetcher(source, config_file_path)
    elif source in ccxt.exchanges:
        return CcxtFetcher(source, config_file_path)
    else:
        raise ValueError(f"Unknown data source: {source}")



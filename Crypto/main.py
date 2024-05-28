import pandas as pd

from Datafetcher.datafetcher import data_fetcher_factory
from Datapreprocessor.preprocessor import DataPreprocessor


def get_preprocessed_data(source: str) -> pd.DataFrame:
    df = data_fetcher_factory(source).fetch_data()
    dataset = DataPreprocessor(df, source).preprocess()
    return dataset


if __name__ == '__main__':
    print(get_preprocessed_data('binance'))

import pandas as pd
import numpy as np
from dataclasses import dataclass
import datetime as dt 

@dataclass
class HQM:
    df: pd.DataFrame
    portfolio_value: float = 100000
    required_col = [
        'One Year Return', 
        'Six Month Return', 
        'Three Month Return', 
        'One Month Return'
    ]

    def _get_null_value(self) -> pd.DataFrame:
        """Return the count of null values in each column."""
        return self.df.isnull().sum()

    def get_stock_stats(self) -> pd.DataFrame:
        try:
            null_values = self._get_null_value()
            if null_values.sum() == 0:
                position_size = self.portfolio_value / len(self.df)
                number_of_share_to_buy = (position_size // self.df.iloc[-1]).astype('int64')

                changes = {}
                periods = {
                    'year5': 252 * 5,
                    'year3': 252 * 3,
                    'year2': 252 * 2,
                    'year1': 252,
                    'month6': 21 * 6,
                    'month3': 21 * 3,
                    'month1': 21,
                    'day30': 30,
                    'day5': 5
                }

                max_value = self.df.max()
                min_value = self.df.min()
                latest_price = self.df.iloc[-1]
                changes['maxChanges'] = ((max_value - min_value) / min_value) * 100

                for period_name, period_number in periods.items():
                    if period_number >= len(self.df):
                        continue
                    past_price = self.df.iloc[-period_number]
                    changes[f"{period_name}ChangePercentage"] = (latest_price - past_price) / past_price * 100

                dataframe = pd.DataFrame.from_dict(changes, orient='index').T
                dataframe['latest Price'] = latest_price
                dataframe['Number of Shares to buy'] = number_of_share_to_buy

                return dataframe
            else:
                raise ValueError(f'Null values found in: {null_values[null_values > 0]}')
        except Exception as e:
            self.get_exception(e)

    def get_momentum_data(self) -> pd.DataFrame:
        try:
            df = self.get_stock_stats()
            if df is None:
                raise ValueError("Failed to get stock stats, cannot proceed.")

            new_df = pd.DataFrame()
            new_df_col = ['latest Price', 'Number of Shares to buy', 'year1ChangePercentage', 'month6ChangePercentage', 'month3ChangePercentage', 'month1ChangePercentage']

            for col in new_df_col:
                if col in df.columns:
                    new_df[col] = df[col]
                    if col not in ['latest Price', 'Number of Shares to buy']:
                        new_df[f'{col}Percentile'] = df[col].rank(pct=True)
                else:
                    new_df[col] = np.nan

            update_col = ['latest Price', 'Number of Shares to buy', 'One Year Return', 'One Year Return Percentile', 'Six Month Return', 
                          'Six Month Return Percentile', 'Three Month Return', 'Three Month Return Percentile', 
                          'One Month Return', 'One Month Return Percentile']

            new_df.columns = update_col

            for col in self.required_col:
                changed_col = col 
                percentile_col = f'{col} Percentile'
                new_df[percentile_col] = new_df[changed_col].rank(pct=True)

            return new_df
        except Exception as e:
            self.get_exception(e)

    def get_hqm_score(self) -> pd.DataFrame:
        try:
            df = self.get_momentum_data()
            if df is None:
                raise ValueError("Failed to get momentum data, cannot proceed.")

            df['HQM Score'] = df[[f'{col} Percentile' for col in self.required_col]].mean(axis=1)
            return df
        except Exception as e:
            self.get_exception(e)

    def get_exception(self, exception):
        print(f'An error occurred: {exception}')


if __name__ == '__main__':

    # Example usage
    ticker_list =  ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA', 'JPM', 'BAC', 'V', 'MA', 'PG', 'KO', 'WMT', 'PEP', 'JNJ', 'UNH', 'PFE', 'LLY']
    stock_df = yf.download(ticker_list, start='2020-01-01', end=dt.date.today(), interval='1D')['Adj Close']
    hqm = HQM(stock_df)
    hqm_score_df = hqm.get_hqm_score()
    print(hqm_score_df)

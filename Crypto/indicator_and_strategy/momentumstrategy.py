import talib 
import pandas as pd, numpy as np
from dataclasses import dataclass
from abc import ABC , abstractmethod
from indicator_and_strategy.indicators import Indicator
import matplotlib.pyplot as plt


class Strategy(ABC):
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def calculate_realized_pnl(self):
        pass

    def calculate_unrealized_pnl(self):
        pass

    def calculate_ppt(self):
        pass

    def calculate_holding_time(self):
        pass

    def calculate_trades(self):
        pass

    def calculate_sharpe_ratio(self):
        pass


    @abstractmethod
    def execute_strategy(self):
        pass


class MomentumStrategy(Strategy):
    def __init__(self, dataset: pd.DataFrame ,short_window: int = 2, long_window: int = 5):
        super().__init__(dataset)
        self.short_window = short_window
        self.long_window = long_window
        self.trades_dates, self.pnls, self.unrlz_dates, self.unrlz_return = self.execute_strategy()

    def _calculate_moving_averages(self):    
        # calculate sma and lma 
        self.closing_price = self.dataset.close
        self.dataset['sma'] = self.closing_price.rolling(window=self.short_window, min_periods=1).mean()
        self.dataset['lma'] = self.closing_price.rolling(window=self.long_window, min_periods=1).mean()

        return self.dataset
    
    def execute_strategy(self):
        self._calculate_moving_averages()
        entry = None
        self.trades_dates = []
        self.pnls = []
        inpos = 0
        self.unrlz_return = []
        self.unrlz_dates = []


        for i in range(len(self.dataset)):
            if i == 0: 
                prv_close = self.dataset['close'][i]
                unrlz = (self.dataset['close'][i] - prv_close) * inpos
            else:   
                unrlz = (self.dataset['close'][i] - self.dataset['close'][i-1]) * inpos

            self.unrlz_return.append(unrlz)
            self.unrlz_dates.append(self.dataset.date[i])

            if self.dataset['sma'][i] > self.dataset['lma'][i] and self.dataset['sma'][i-1] <= self.dataset['lma'][i-1]:
                if entry:
                    pnl = entry - self.dataset['close'][i]
                    self.pnls.append(pnl)
                    self.trades_dates.append(self.dataset.date[i])
                entry = self.dataset['close'][i]
                inpos = 1

            elif self.dataset['sma'][i] < self.dataset['lma'][i] and self.dataset['sma'][i-1] >= self.dataset['lma'][i-1]:
                if entry:
                    pnl = self.dataset['close'][i] - entry
                    self.pnls.append(pnl)
                    self.trades_dates.append(self.dataset.date[i])
                entry = self.dataset['close'][i]
                inpos = -1

        return self.trades_dates, self.pnls, self.unrlz_dates, self.unrlz_return


    def visualize_strategy(self):
        plt.figure(figsize=(16,8))
        plt.title('Unrealized PnL vs Realized PnL')
        plt.plot(self.unrlz_dates, np.cumsum(self.unrlz_return))
        plt.plot(self.trades_dates, np.cumsum(self.pnls), '-o')
        plt.axhline(y=0, color='black', linestyle='--')
        
        return plt.show()


    def calculate_realized_pnl(self):
        return np.cumsum(self.pnls)


    def calculate_unrealized_pnl(self):
        return np.cumsum(self.unrlz_return)
    

    def calculate_ppt(self):
        return np.mean(self.pnls)
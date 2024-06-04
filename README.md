# RL-Project
- Total state space dimension = OHLC features + Indicator features + Holding/Balance features + Strategy signal feature
  -                              = 4 + 4 + 2 + 1
  -                              = 11
- Discrete Features need to be encoding using one-hot encoding before feeding, current holding(long, short no position into (e.g., [1, 0, 0]), short (e.g., [0, 1, 0]), or no position (e.g., [0, 0, 1]).

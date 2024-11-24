import pandas as pd

TRDX = pd.read_csv("Stocksim/plot/data/tickers.csv",header=None, index_col=0, names=["name"]).to_dict()["name"]
print(TRDX)
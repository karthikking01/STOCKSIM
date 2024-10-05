from datetime import * 
import pandas as pd
import numpy as np
dt = date.today()-timedelta(days=3650)
cols = []
for i in range(7):
    cols.append(str(dt+timedelta(days=i)))
stock = pd.DataFrame(columns=cols)
print(stock)
print(cols)
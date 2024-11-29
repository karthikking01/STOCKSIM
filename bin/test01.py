import pandas as pd
from datetime import *
from plot.data import *

led = ledger("bin\plot\data\ledger.csv")
print(led.data["date"])
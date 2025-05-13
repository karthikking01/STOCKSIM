import pandas as pd
dict = {"one":1,"two":2,"three":3, 'seven':7}
s1 = pd.Series(dict)
s1['four'] = 4
print(s1)
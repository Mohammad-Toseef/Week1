import pandas as pd
import matplotlib.pyplot as plt
PATH = 'C:/Users/Mohammad Touseef/Documents/'
CSV_FILE_NAME = 'Crypto.csv'
df = pd.read_csv(PATH+CSV_FILE_NAME)
df_sort = df.sort_values('current_price')
df_sort[:40].plot(x='id', y='current_price',kind = 'bar')
plt.show()
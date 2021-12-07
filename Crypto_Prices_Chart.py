import pandas as pd
import matplotlib.pyplot as plt
PATH = 'C:/Users/Mohammad Touseef/Documents/'
CSV_FILE_NAME = 'Crypto.csv'
#reading Crypto Csv File to dataframe
df = pd.read_csv(PATH+CSV_FILE_NAME)
#sorting the dataframe in ascending order
df_sort = df.sort_values('current_price')
#Bar Chart Plotting
df_sort[:20].plot(x='id', y='current_price',kind = 'bar')
plt.title('Crypto Prices ') #title of Chart
plt.xticks(rotation = 70) #rotating x axis markers
plt.ylabel('Current Price in USD') #y axis label
plt.legend(loc='best')
for i in range(len(df_sort[:20])):
    price = '{:.3f}'.format(df_sort[:20]['current_price'].values[i])
    plt.text(i,float(price),float(price),ha = 'center')
plt.show()
#Pie Chart
df_sort[:5].plot(x='id',y='current_price',kind = 'pie',labels = [x for x in df_sort[:5]['id']],autopct='%1.0f%%')
plt.title('Crypto Prices')
plt.legend(loc='upper left')
plt.show()
#Histogram
df_sort[:40].plot(x='id',y='current_price',kind = 'hist')
plt.title('Crypto Prices ')
plt.show()
#box
df_sort[:40].plot(x='id',y='current_price',kind = 'box')
plt.title('Crypto Prices ')
plt.show()

#line chart

line1 = df_sort[:10].plot.line(x='id', y='current_price', label="Crypto Prices")
plt.title("line chart of Crypto Prices")
plt.ylabel('Current Price in USD')
plt.show()
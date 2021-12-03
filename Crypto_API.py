#Module to send http requests to server
import requests
#Module to utilize excel ,csv , pdf
import pandas as pd
import lxml
import pdfkit
#sending request to server and storing response in variable
response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h")
#normalizing the json
pf = pd.json_normalize(response.json())
#generating csv file
pf.to_csv('C:/Users/Mohammad Touseef/Documents/Crypto.csv',index=False)
#reading csv file
df = pd.read_csv('C:/Users/Mohammad Touseef/Documents/Crypto.csv')
Excel_writer = pd.ExcelWriter('C:/Users/Mohammad Touseef/Documents/Crypto.xlsx')
#storing data in excel file
df.to_excel(Excel_writer,index = False)
#saving the file
Excel_writer.save()
#Generating html file
c=0
for item in df['image']:
    df['image'][c] = '<img src="'+str(item)+'" width = 50>'
    c+=1
df.to_html('C:/Users/Mohammad Touseef/Documents/Crypto.html',escape=False)
#generating xml file
df.to_xml('C:/Users/Mohammad Touseef/Documents/Crypto.xml')
#generating pdf file
pdfkit.from_file('C:/Users/Mohammad Touseef/Documents/Crypto.html','C:/Users/Mohammad Touseef/Documents/Crypto.pdf')
'''
html_result = json2html.convert(json=response.json())
with open('C:/Users/Mohammad Touseef/Documents/Crypto.html','w') as html:
    html.write(str(html_result))
xml = dicttoxml()
'''
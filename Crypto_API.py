'''This script fetches crypto information and generates html,excel, pdf, xml,
   csv files of the output'''
#Module to send http requests to server
import requests
#Module to utilize excel ,csv , pdf
import pandas as pd
import lxml
import pdfkit
import numpy as np
#sending request to server and storing response in variable
def to_CSV(JSON,Path_with_File_Name):
    df = pd.json_normalize(JSON)
    df.to_csv(Path_with_File_Name,index=False)

def CSV_to_Excel(CSV_DF,Path_with_File_Name):
    Excel_Writer = pd.ExcelWriter(Path_with_File_Name)
    CSV_DF.to_excel(Excel_Writer,index= False)
    Excel_Writer.save()

def CSV_to_HTML(CSV_DF,Path_with_File_Name):
    index=0
    for item in CSV_DF['image']:
        url = CSV_DF['image'][index].split('.png')[0]+'.png'
        CSV_DF["image"].at[index] = '<img src="' + str(url) + '" width = 50>'
        index+=1
    CSV_DF.to_html(Path_with_File_Name,escape=False)

def CSV_to_XML(CSV_DF,Path_with_File_Name):
    CSV_DF.to_xml(Path_with_File_Name)

def HTML_to_PDF(HTML_FILE_PATH,PDF_FILE_PATH):
    options = {
        'page-size': 'B0',
        'dpi': 400
    }
    pdfkit.from_file(HTML_FILE_PATH,PDF_FILE_PATH,options=options)
response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h")
#generating CSV File from JSON
PATH = 'C:/Users/Mohammad Touseef/Documents/'
CSV_FILE_NAME = 'Crypto.csv'
CSV = PATH + CSV_FILE_NAME
to_CSV(response.json(),CSV)

#CSV Dataframe
csv_dataframe = pd.read_csv(CSV,na_values=['none'])
csv_dataframe = csv_dataframe.replace(np.nan, '', regex=True) # All data frame
#Generating Excel File From CSV Dataframe
Excel_File_Name = 'Crypto.xlsx'
CSV_to_Excel(csv_dataframe,PATH+Excel_File_Name)

#Generating HTML file from CSV Dataframe
HTML_File_Name = 'Crypto.html'
CSV_to_HTML(csv_dataframe,PATH+HTML_File_Name)

#Generating XML File from CSV Dataframe
XML_File_Name = 'Crypto.xml'
CSV_to_XML(csv_dataframe,PATH+XML_File_Name)

#Generating PDF File from HTML
PDF_File_Name = 'Crypto.pdf'
HTML_to_PDF(PATH+HTML_File_Name,PATH+PDF_File_Name)











'''pf = pd.json_normalize(response.json())
#generating csv file
#pf.to_csv('C:/Users/Mohammad Touseef/Documents/Crypto.csv',index=False)
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
'''
html_result = json2html.convert(json=response.json())
with open('C:/Users/Mohammad Touseef/Documents/Crypto.html','w') as html:
    html.write(str(html_result))
xml = dicttoxml()
'''
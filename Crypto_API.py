'''This script fetches crypto Prices information and generates html,excel, pdf, xml,
   csv files of the response received from API    Author - Mohammad Toseef '''

import requests
import pandas as pd
import pdfkit
import numpy as np
import logging

logging.basicConfig(filename='Crypto.log', level=logging.DEBUG)

#Function to normalize JSON data fetched from API and saving it as csv File
# inputs
def JSON_to_CSV(JSON, path_with_file_name):
    df = pd.json_normalize(JSON)
    df.to_csv(path_with_file_name, index = False)
    logging.debug('CSV File has been Generated : Path - {}'.format(path_with_file_name))
    return df

#Function to convert CSV file to an Excel File
def CSV_to_Excel(CSV_DF,path_with_file_name):
    Excel_Writer = pd.ExcelWriter(path_with_file_name)
    CSV_DF.to_excel(Excel_Writer,index= False)
    Excel_Writer.save()
    logging.debug('Excel file has been generated : Path - {}'.format(path_with_file_name))

#Function to convert CSV File to HTML File after processing images url
def CSV_to_HTML(CSV_DF,path_with_file_name):
    index = 0
    for item in CSV_DF['image']:
        url = item.split('.png')[0] + '.png'
        CSV_DF["image"].at[index] = '<img src="' + str(url) + '" width = 50>'
        index += 1
    CSV_DF.to_html(path_with_file_name,escape=False)
    logging.debug('HTML is generated from CSV : Path - {}'.format(path_with_file_name))

#Function to convert CSV Files to XML Files
def CSV_to_XML(CSV_DF,path_with_file_name):
    CSV_DF.to_xml(path_with_file_name)
    logging.debug('XML file has been generated : Path - {}'.format(path_with_file_name))

#Converts HTML to pdf using pdfkit module
def HTML_to_PDF(HTML_FILE_PATH,PDF_FILE_PATH):
    options = {
        'page-size': 'B0',
        'dpi': 400
    }
    pdfkit.from_file(HTML_FILE_PATH,PDF_FILE_PATH,options=options)
    logging.debug('PDF File has been Generated : Path {}'.format(PDF_FILE_PATH))

#Request API to fetch information
response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h")
logging.debug(response)
PATH = 'C:/Users/Mohammad Touseef/Documents/'           # don't hardcode the path
CSV_FILE_NAME = 'Crypto.csv'
CSV = PATH + CSV_FILE_NAME

#CSV File Generation
csv_dataframe = JSON_to_CSV(response.json(),CSV)
csv_dataframe = csv_dataframe.replace(np.nan, '', regex=True) # All data frame

#Excel File Generation
Excel_File_name = 'Crypto.xlsx'
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
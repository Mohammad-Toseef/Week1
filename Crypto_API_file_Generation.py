'''This script fetches crypto Prices information and generates html,excel, pdf, xml,
   csv files of the response received from API    Author - Mohammad Toseef '''

import requests
import pandas as pd
import pdfkit
import numpy as np
import logging

logging.basicConfig(filename='Crypto.log', level=logging.DEBUG)

# Function to normalize JSON data fetched from API and saving it as csv File
def JSON_to_CSV(JSON, path_with_file_name):
    '''
    :param JSON: Json object having data which is to be normalized
    :param path_with_file_name: name of the csv file in which data will be saved
    :return: returns the dataframe containing normalized Crypto data
    '''
    df = pd.json_normalize(JSON)
    df.to_csv(path_with_file_name, index = False)
    logging.debug('CSV File has been Generated : Path - {}'.format(path_with_file_name))
    return df

#Function to convert CSV file to an Excel File
def CSV_to_Excel(CSV_DF,path_with_file_name):
    '''
    :param CSV_DF: This parameter takes dataframe having csv file data
    :param path_with_file_name: This parameter takes Excel file name as input
    :return: None
    '''
    Excel_Writer = pd.ExcelWriter(path_with_file_name)
    CSV_DF.to_excel(Excel_Writer,index= False)
    Excel_Writer.save()
    logging.debug('Excel file has been generated : Path - {}'.format(path_with_file_name))

#Function to convert CSV File to HTML File after processing images url
def CSV_to_HTML(CSV_DF,path_with_file_name):
    '''
    :param CSV_DF: This parameter takes dataframe (having csv file data) as input
    :param path_with_file_name: This parameter takes HTML file name as input
    :return: None
    '''
    index = 0
    for item in CSV_DF['image']:
        url = item.split('.png')[0] + '.png'
        CSV_DF["image"].at[index] = '<img src="' + str(url) + '" width = 50>'
        index += 1
    CSV_DF.to_html(path_with_file_name,escape=False)
    logging.debug('HTML is generated from CSV : Path - {}'.format(path_with_file_name))

#Function to convert CSV Files to XML Files
def CSV_to_XML(CSV_DF,path_with_file_name):
    '''
    :param CSV_DF:  This parameter takes dataframe (having csv file data) as input
    :param path_with_file_name: This parameter takes XML file name as input
    :return: None
    '''
    CSV_DF.to_xml(path_with_file_name)
    logging.debug('XML file has been generated : Path - {}'.format(path_with_file_name))

#Converts HTML to pdf using pdfkit module
def HTML_to_PDF(HTML_FILE_PATH,PDF_FILE_PATH):
    '''
    :param HTML_FILE_PATH:  This parameter takes HTML file name as input
    :param PDF_FILE_PATH: This parameter takes PDF file name as input
    :return: None
    '''
    options = {
        'page-size': 'B0',
        'dpi': 400
    }
    pdfkit.from_file(HTML_FILE_PATH,PDF_FILE_PATH,options=options)
    logging.debug('PDF File has been Generated : Path {}'.format(PDF_FILE_PATH))


#Request API to fetch information
response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h")
logging.debug(response)
csv_file_name = 'Crypto.csv'

#CSV File Generation
csv_dataframe = JSON_to_CSV(response.json(),csv_file_name)
csv_dataframe = csv_dataframe.replace(np.nan, '', regex=True) # All data frame

#Excel File Generation
excel_file_name = 'Crypto.xlsx'
CSV_to_Excel(csv_dataframe,excel_file_name)

#Generating HTML file from CSV Dataframe
html_file_name = 'Crypto.html'
CSV_to_HTML(csv_dataframe,html_file_name)

#Generating XML File from CSV Dataframe
XML_file_name = 'Crypto.xml'
CSV_to_XML(csv_dataframe,XML_file_name)

#Generating PDF File from HTML
PDF_file_name = 'Crypto.pdf'
HTML_to_PDF(html_file_name,PDF_file_name)
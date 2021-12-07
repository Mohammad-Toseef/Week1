'''This script fetches crypto Prices information and generates html,excel, pdf, xml,
   csv files of the response received from API    Author - Mohammad Toseef '''

import requests
import pandas as pd
import pdfkit
import numpy as np
import logging

logging.basicConfig(filename='Crypto.log', level=logging.DEBUG)

# Function to normalize JSON data fetched from API and saving it as csv File
def JSON_to_CSV(JSON, file_name):
    '''
    Normalize JSON data fetched from API and save it in CSV format
    :param JSON (json): Json object having data which is to be normalized
    :param file_name (str): name of the csv file where data will be saved
    :return:  dataframe containing normalized Crypto data
    '''
    df = pd.json_normalize(JSON)
    df.to_csv(file_name, index = False)
    logging.debug('CSV File has been Generated : Path - {}'.format(file_name))
    return df

#Function to convert CSV file to an Excel File
def CSV_to_Excel(csv_df, file_name):
    '''
    Convert dataframe to Excel
    :param csv_df:  takes dataframe having csv file data
    :param file_name: This parameter takes Excel file name as input
    :return: None
    '''
    Excel_Writer = pd.ExcelWriter(file_name)
    csv_df.to_excel(Excel_Writer, index = False)
    Excel_Writer.save()
    logging.debug('Excel file has been generated : Path - {}'.format(file_name))

#Function to convert CSV File to HTML File after processing images url
def CSV_to_HTML(csv_df, file_name):
    '''
    :param csv_df: This parameter takes dataframe (having csv file data) as input
    :param file_name: This parameter takes HTML file name as input
    :return: None
    '''
    index = 0
    for item in csv_df['image']:
        url = item.split('.png')[0] + '.png'
        csv_df["image"].at[index] = '<img src="' + str(url) + '" width = 50>'
        index += 1
    csv_df.to_html(file_name, escape = False)
    logging.debug('HTML is generated from CSV : Path - {}'.format(file_name))

#Function to convert CSV Files to XML Files
def CSV_to_XML(csv_df, file_name):
    '''
    :param csv_df:  This parameter takes dataframe (having csv file data) as input
    :param file_name: This parameter takes XML file name as input
    :return: None
    '''
    csv_df.to_xml(file_name)
    logging.debug('XML file has been generated : Path - {}'.format(file_name))

#Converts HTML to pdf using pdfkit module
def HTML_to_PDF(html_file_path, pdf_file_path):
    '''
    :param html_file_path:  This parameter takes HTML file name as input
    :param pdf_file_path: This parameter takes PDF file name as input
    :return: None
    '''
    options = {
        'page-size': 'B0',
        'dpi': 400
    }
    pdfkit.from_file(html_file_path, pdf_file_path, options = options)
    logging.debug('PDF File has been Generated : Path {}'.format(pdf_file_path))


#Request API to fetch information
response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h%2C24h")
logging.debug(response)
csv_file_name = 'Crypto.csv'

#CSV File Generation
csv_dataframe = JSON_to_CSV(response.json(), csv_file_name)
csv_dataframe = csv_dataframe.replace(np.nan, '' , regex = True) # All data frame

#Excel File Generation
excel_file_name = 'Crypto.xlsx'
CSV_to_Excel(csv_dataframe, excel_file_name)

#Generating HTML file from CSV Dataframe
html_file_name = 'Crypto.html'
CSV_to_HTML(csv_dataframe, html_file_name)

#Generating XML File from CSV Dataframe
XML_file_name = 'Crypto.xml'
CSV_to_XML(csv_dataframe, XML_file_name)

#Generating PDF File from HTML
PDF_file_name = 'Crypto.pdf'
HTML_to_PDF(html_file_name, PDF_file_name)
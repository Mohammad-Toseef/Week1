'''This script fetches crypto Prices information and generates html,excel, pdf, xml,
   csv files of the response received from API    Author - Mohammad Toseef '''
import json
import sys
import requests
import pandas as pd
import pdfkit
import numpy as np
import logging
import os
import re


logging.basicConfig(filename = 'demo.log', level= logging.DEBUG,
                    format = '%(asctime)s // %(levelname)s : %(message)s // line no. %(lineno)d',
                    filemode = 'w')

def json_to_csv(JSON, file_name):
    '''
    Normalize JSON data fetched from Crypto API and save it as CSV file
    :param JSON (json): Json object having data which is to be normalized
    :param file_name (str): name of the csv file where data will be saved
    :return:  dataframe containing normalized Crypto data
    '''
    df = pd.json_normalize(JSON)
    df.to_csv(file_name, index = False)
    return df
    logging.debug('CSV File has been Generated : Filename - {}'.format(file_name))

def to_excel(csv_df, file_name):
    '''
    Saves dataframe as Excel
    :param csv_df:  takes dataframe having csv file data
    :param file_name: takes Excel file name as input
    :return: None
    '''
    try:
        if not isinstance(csv_df,pd.DataFrame) :
            raise AttributeError('csv_df arg in to_excel() is not a dataframe')
            if not isinstance(file_name,str) and not file_name.endswith('.xlsx'):
                raise NameError('Please Provide Valid Excel File Name')
        Excel_Writer = pd.ExcelWriter(file_name)
        csv_df.to_excel(Excel_Writer, index = False)
        Excel_Writer.save()
        logging.debug('Excel file has been generated : Filename - {}'.format(file_name))
    except NameError as ne:
        logging.error(ne)
    except AttributeError as ae:
        logging.error(ae)
    except PermissionError:
        logging.error('Got Permission Error while trying to write Excel File')
    '''
    Excel_Writer = pd.ExcelWriter(file_name)
    csv_df.to_excel(Excel_Writer, index=False)
    Excel_Writer.save()
    '''

def to_html(csv_df, file_name):
    '''
    Saves dataframe as HTML File
    :param csv_df: takes dataframe (having csv file data) as input
    :param file_name: takes HTML file name as input
    :return: None
    '''
    try:
        if not isinstance(csv_df,pd.DataFrame) :
            raise AttributeError('csv_df arg in to_html() is not a dataframe')
            if not isinstance(file_name,str) and not file_name.endswith('.html') :
                raise NameError('Please Provide Valid HTML File Name')
        index = 0
        # converting urls in image column to its corresponding html <img> tag
        for item in csv_df['image']:
            url = item.split('.png')[0] + '.png'
            csv_df["image"].at[index] = '<img src="' + str(url) + '" width = 50>'
            index += 1
        csv_df.to_html(file_name, escape = False)
        logging.debug('HTML is generated from CSV : Filename - {}'.format(file_name))
    except AttributeError as e:
        logging.error(e)
    except NameError as ne:
        logging.error(ne)
    except PermissionError:
        logging.error('Got Permission Error while trying to write HTML File')

def to_xml(csv_df, file_name):
    '''
    Saves dataframe as XML File
    :param csv_df:  takes dataframe (having csv file data) as input
    :param file_name: takes XML file name as input
    :return: None
    '''
    try:
        if not isinstance(csv_df,pd.DataFrame) :
            raise AttributeError('csv_df arg in to_xml() is not a dataframe')
            if not isinstance(file_name,str) and not file_name.endswith('.xml') :
                raise NameError('Please Provide Valid XML File Name')
        csv_df.to_xml(file_name)
        logging.debug('XML file has been generated : Filename - {}'.format(file_name))
    except AttributeError as e:
        logging.error(e)
    except NameError as ne:
        logging.error(ne)
    except PermissionError:
        logging.error('Got Permission Error while trying to write HTML File')

def html_to_pdf(html_file_name, pdf_file_name):
    '''
    Converts HTML file to PDF
    :param html_file_name:  This parameter takes HTML file name as input
    :param pdf_file_name: This parameter takes PDF file name as input
    :return: None
    '''
    try:
        if not isinstance(html_file_name, str) or not html_file_name.endswith('.html'):
            raise NameError('Please Provide Valid HTML file name')
            if not isinstance(pdf_file_name, str) or not pdf_file_name.endswith('.pdf'):
                raise NameError('Pleaes provide valid pdf file name')
        options = {
            'page-size': 'B0',
            'dpi': 400
        }
        pdfkit.from_file(html_file_name, pdf_file_name, options = options)
        logging.debug('PDF File has been Generated : Filename {}'.format(pdf_file_name))
    except NameError as ne:
        logging.error(ne)
    except FileNotFoundError as fnfe:
        logging.error('file is not present')
        logging.exception(fnfe)
    except OSError as ose:
        logging.error(ose)


try:
    #checking if CSV File is present in current directory or not
    if os.path.isfile( os.path.dirname(os.path.realpath(__file__)) + '\Crypto.csv'):
        csv_dataframe = pd.read_csv('Crypto.csv')
    else:
        # Fetching data from API in case of CSV file not present
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&"
                                + "order=market_cap_desc&per_page=100&page=1&sparkline=false&price_"
                                + "change_percentage=1h%2C24h")
#       response = requests.get('no.com')
        csv_file_name = 'Crypto.csv'
        csv_dataframe = json_to_csv(response.json(), csv_file_name)
        logging.info('Status Code : ' + str(response.status_code))
        if response.status_code >= 400:
            raise ConnectionError
except requests.exceptions.RequestException as e:
    logging.error('Error in establishing connection with API ')
    logging.exception(e)
    sys.exit(1)
except json.JSONDecodeError as e:
    logging.error('JSON data in response is not correct ')
    logging.exception(e)
    sys.exit(1)
except ConnectionError as ce:
    logging.error('A Connection error occured ')
    logging.exception(ce)
    sys.exit(1)
else:
    logging.info("Crypto.csv is available")

csv_dataframe = csv_dataframe.replace(np.nan, '' , regex = True)    # Replacing NaN values with whitespace

#Excel File Generation
excel_file_name = 'Crypto.xlsx'
to_excel(csv_dataframe, excel_file_name)

#Generating HTML file from CSV Dataframe
html_file_name = 'Crypto.html'
to_html(csv_dataframe, html_file_name)

#Generating XML File from CSV Dataframe
xml_file_name = 'Crypto.xml'
to_xml(csv_dataframe, xml_file_name)

#Generating PDF File from HTML
pdf_file_name = 'Crypto.pdf'
html_to_pdf(html_file_name, pdf_file_name)
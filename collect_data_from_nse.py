"""
Script for downloading data from nse and adding it to a csv file
"""
import ssl
import re
import urllib3
import os
import pandas as pd
from bs4 import BeautifulSoup

FILENAME = 'data/stocks.csv'

def get_data_frame():
    """
    Returns stock data got from
    https://www.nse.co.ke/market-statistics/equity-statistics.html?view=statistics
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    http = urllib3.PoolManager()
    html_data = http.request('GET',
                             'https://www.nse.co.ke/market-statistics/equity-statistics.html?view=statistics').data
    soup = BeautifulSoup(html_data, "html.parser").select('.marketStats')[0]
    table_contents = soup.find_all(class_=re.compile('row[0,1]'))
    table_header = soup.select('.tablelistHeader')[0]
    final_table = '<table>' + str(table_header) + str(table_contents) + '</table>'
    dataframes = pd.read_html(final_table, header=0)
    return dataframes[0]

def remove_nums_from_name(dataframe):
    """
    Removes ints from company names e.g Saf5.00 becomes Saf
    """
    dataframe['Company'] = dataframe['Company'].str.replace(r'\d+\.\d+', '')
    dataframe['Company'] = dataframe['Company'].str.strip()
    return dataframe

def save_current_stocks():
    """
    TODO: save stocks in csv file
    """
    stock_frame = remove_nums_from_name(get_data_frame())

    if os.path.exists(FILENAME):
        append_write = 'a'
        header = False
    else:
        append_write = 'w'
        header = True

    stock_frame.to_csv(FILENAME, mode=append_write, index=False, header=header)
    #  print(stock_frame.to_string())

if __name__ == '__main__':
    save_current_stocks()

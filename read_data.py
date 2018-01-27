import re
import pandas as pd


SHARE_BLOCKS = 100

def get_data_frame():
    """
    Returns data frame containing all stocks info listed on
    http://www.wazua.co.ke/investor/stockssummary.aspx
    """
    table_headers = ['agricultural',
                     'commercial_and_services',
                     'finance_and_investment',
                     'industrial_and_allied',
                     'alternative_investment_segment']
    dfs = pd.read_html('http://www.wazua.co.ke/investor/stockssummary.aspx',
                       header=0,
                       attrs={'id' : re.compile(r"ctl00_ContentPlaceHolder1_GridView\d+")})
    for index, table in enumerate(dfs):
        table['sector'] = table_headers[index]
    stock = pd.concat(dfs)
    return stock.rename(columns={'Mkt Cap. (Mn)':'mkt_cap', 'P/ E':'P/E'})

def get_stocks_within_range(max_amount, dataframe):
    """
    Returns stocks that can be bought with the max amount set
    """
    max_per_share = max_amount / SHARE_BLOCKS
    return dataframe.query('Price <= %s' %max_per_share)

def remove_negative_eps(dataframe):
    """
    Removes all loss making companies
    """
    return dataframe.query('EPS >= 0')

def remove_aims_stocks(dataframe):
    """
    Removes stocks in aims group coz they aren't that active"
    """
    return dataframe.query('sector != "alternative_investment_segment"')

def remove_stocks_less_dividend(dividend, dataframe):
    """
    Removes stocks that pay less than specified divident
    """
    return dataframe.query('DPS >= %s' %dividend)



dataf = get_data_frame()
stocks_in_range = get_stocks_within_range(5000, dataf)
non_negatives = remove_negative_eps(stocks_in_range)
less_aims_stocks = remove_aims_stocks(non_negatives)
divident_stocks = remove_stocks_less_dividend(0.5, less_aims_stocks)
print(divident_stocks.to_string(index=False))

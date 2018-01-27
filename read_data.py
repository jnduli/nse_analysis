"""
Script for picking up data and analyzing best stocks to buy
"""
import re
import argparse
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

def create_parser():
    """
    Creates the argument parser in use
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_price',
                        help='Maximum Amount to spend on shares',
                        default=5000, type=int)
    parser.add_argument('--add_aims',
                        help='Add Alternative Investment Stocks',
                        action="store_true")
    parser.add_argument('--add_loss_makers',
                        help='Add loss making companies to result',
                        action="store_true")
    parser.add_argument('--minimum_dividend',
                        help='Set the minimum divident to check. Defaults to 0',
                        default=0,
                        type=float)
    parser.add_argument('--order_by_PE_DPS',
                        help='Order results by P/E values and then DPS value',
                        action='store_true')
    args = parser.parse_args()
    print_result(args.max_price, args.add_aims,
                 args.add_loss_makers, args.minimum_dividend, args.order_by_PE_DPS)

def print_result(max_price, add_aims, add_loss_makers, minimum_dividend, order_by_pe_dps):
    """
    Print table containing stocks that meet criteria
    """
    data = get_data_frame()
    if add_aims is False:
        data = remove_aims_stocks(data)
    if add_loss_makers is False:
        data = remove_negative_eps(data)

    data = get_stocks_within_range(max_price, data)
    data = remove_stocks_less_dividend(minimum_dividend, data)
    if order_by_pe_dps:
        data = data.sort_values(by=['P/E', 'DPS'], ascending=[True, False])
    print(data.to_string(index=True))

if __name__ == '__main__':
    create_parser()

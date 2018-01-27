##################
NSE Stock Analysis
##################

I've based this script off the advice found frm the following
links:

+ `Link 1 <http://www.figures.co.ke/Articles/2017/26-Nov-17_Investing_In_Listed_Shares-I.html>`_
+ `Link 2  <http://www.figures.co.ke/Articles/2017/03-Dec-17_Investing_In_Listed_Shares-II.html>`_

The nse stock data is found from wazua, and here is the link I
use:

+ `wazua_stocks <http://www.wazua.co.ke/investor/stockssummary.aspx>`_

The script loads the data from the above website. To use the
script, you need to have some things installed:

+ Python3
+ Pandas: `Install instructions  <https://pandas.pydata.org/>`_

After installine the same, you can do

.. code-block:: bash

    python read_data.py -h

To get usage instructions.


Example Commands
================

.. code-block:: bash

    python read_data.py

The above command selects all stocks you can buy with Ksh 5000
(stocks can be bought in lumpsums of 100). It also removes the
aims and loss making stocks from the list displayed, and shows
stocks with all dividends.

.. code-block:: bash

    python read_data.py --max_price 10000 --add_aims
    --add_loss_makers --minimum_dividend 0.5 --order_by_PE_DPS

The above command selects all stocks you can buy with Ksh 10000.
The list will also include aims (alternative investment segment)
stocks and also stocks that make losses. It will finally order the
stocks by P/E ascending and DPS descending.

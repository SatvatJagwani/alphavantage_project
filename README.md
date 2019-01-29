# alphavantage_project

This project focuses on plotting the different patterns of users querying the stock prices. There are three component files (as of now):

visualize_data.py:
This provides the function for plotting the frequency of queries in a set of stock symbols for a particular function (or all functions), a particular interval (or all intervals), and a particular set of user IPs (or all users) for the dates 12/09/2018 till 12/22/2018.
This script assumes that there is a folder alphavantage_data/ which contains files 2018-12-09.csv, 2018-12-10.csv, ... 2018-12-22.csv, each with five columns: timestamp, ipaddress, symbol, function, interval.


visualize_stock_prices_queries.py:
This python script plots the query frequency and daily price variation for a group of stocks. One plot is generated for all the stock frequencies of all the stocks but n different plots are generated for prices of n different stock symbols.
Assumptions are same as the one in visulaize_data.py
Relative prices refer to Simple Moving Average (SMA) of closing prices.


print_common_ips.py:
This python script does two possible functions:

If a particular date is specified, it prints:
the query pattern of each stock symbol for that date, 
all ips such that each queried all the symbols in the list of stocks, and
the query pattern of these stock symbols for the selected ips on that date.

If no particular date is specified, it plots:
The query pattern of each stock symbol in the specified list, and
The query patterns of all stock symbols for the set of ips which queried all the listed stock symbols.

Assumptions are same as the one in visualize_data.py.


An extra file (US Stock Symbols - US Stock Symbols.csv) is used for selecting the default set of stock symbols and for getting stock name corresponding to a symbol.

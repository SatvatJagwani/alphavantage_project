import pandas as pd
import matplotlib.pyplot as plt
from visualize_data import plot_queries_for_symbols
from datetime import datetime

symbol_list = input("Which symbols to check? (space separated) ").split(' ')
date = input("Which date? (YYYY-MM-DD) ")
function = input("Function? ")
interval = input("Interval? ")
if date:
  df = pd.read_csv('alphavantage_data/' + date + '.csv')
  filtered_df = df[df['symbol'].isin(symbol_list) & (df['function']==function if function else True) & (df['interval']==interval if interval else True)]
  print(filtered_df['symbol'].value_counts())
  common_ips = set(filtered_df['ipaddress'].unique())
  for symbol in symbol_list:
    common_ips = common_ips & set(filtered_df[filtered_df['symbol']==symbol]['ipaddress'].unique())
  print(filtered_df[filtered_df['ipaddress'].isin(common_ips)]['symbol'].value_counts())
  print(common_ips)
else:
  full_stock_frequencies = []
  common_stock_frequencies = []
  all_days_common_ips = set()
  for i in ['09'] + [str(i) for i in range(10, 23)]:
    df = pd.read_csv('alphavantage_data/2018-12-' + i + '.csv')
    filtered_df = df
    if function:
      filtered_df = filtered_df[filtered_df['function']==function]
    if interval:
      filtered_df = filtered_df[filtered_df['interval']==interval]
    specific_symbols_df = filtered_df[filtered_df['symbol'].isin(symbol_list)]
    full_stock_frequencies.append(specific_symbols_df['symbol'].value_counts().rename('2018-12-' + i))
    common_ips = set(specific_symbols_df['ipaddress'].unique())
    for symbol in symbol_list:
      common_ips = common_ips & set(specific_symbols_df[specific_symbols_df['symbol']==symbol]['ipaddress'].unique())
    all_days_common_ips = all_days_common_ips | common_ips
    #common_stock_frequencies.append(filtered_df[filtered_df['ipaddress'].isin(common_ips)]['symbol'].value_counts().rename('2018-12-' + i))
  full_frequency_df = pd.concat(full_stock_frequencies, axis=1).T
  print(full_frequency_df)
  full_frequency_df['dates'] = full_frequency_df.index
  full_frequency_df['dates'] = full_frequency_df['dates'].apply(lambda x: int(x[-2:]))
  spec_stocks = full_frequency_df.columns.tolist()
  spec_stocks.remove('dates')
  full_frequency_df.plot.line(x='dates', y=spec_stocks, marker='o')
  plt.title('original')
  #common_frequency_df = pd.concat(common_stock_frequencies, axis=1).T
  #print(common_frequency_df)
  #common_frequency_df['dates'] = common_frequency_df.index
  #common_frequency_df['dates'] = common_frequency_df['dates'].apply(lambda x: int(x[-2:]))
  #all_stocks = common_frequency_df.columns.tolist()
  #all_stocks.remove('dates')
  #common_frequency_df.plot.line(x='dates', y=all_stocks, marker='o')
  plot_queries_for_symbols(function=function, interval=interval, ips=all_days_common_ips)
  plt.title('common ips')
  plt.show()

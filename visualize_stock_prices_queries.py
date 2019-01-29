import pandas as pd
import matplotlib.pyplot as plt
import visualize_data
from datetime import datetime

symbol_list = input("Which symbols to check? (space separated) ").split(' ')
small_companies = input("Are these small companies? ")
use_relative_price = input("Use relative price? ")
plot_market_price = input("Plot market price? ")
visualize_data.plot_queries_for_symbols(symbol_list, use_full_stock_name=True)

market_prices = pd.read_csv('price_data/daily_DJIA.csv')
dates = ['2018-12-'+str(i) for i in range(10, 32)] + ['2019-01-0'+str(i) for i in range(1, 10)]+ ['2019-01-'+str(i) for i in range(10, 32)]
if plot_market_price:
  market_prices['dates'] = market_prices['timestamp'].apply(lambda x: (datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]))-datetime(2018,11,30)).days)
  selected_market_prices = market_prices[market_prices['timestamp'].isin(dates)].set_index('timestamp')
  selected_market_prices.plot.line(x='dates', y=['open','high','low','close'])
  #plt.ylim(ymin=0)
  plt.title('Market prices')
market_prices = market_prices.set_index('timestamp')

for symbol in symbol_list:
  if small_companies:
    prices = pd.read_csv('price_data/small_co/daily_'+symbol+'.csv')
  else:
    prices = pd.read_csv('price_data/daily_'+symbol+'.csv')
  prices['dates'] = prices['timestamp'].apply(lambda x: (datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]))-datetime(2018,11,30)).days)
  selected_prices = prices[prices['timestamp'].isin(dates)].set_index('timestamp')
  if use_relative_price:
    selected_prices['market_open'] = market_prices['open']
    selected_prices['market_high'] = market_prices['high']
    selected_prices['market_low'] = market_prices['low']
    selected_prices['market_close'] = market_prices['close']
    selected_prices['rel_open'] = selected_prices.apply(lambda row: row[0]/row[6], axis=1)
    selected_prices['rel_high'] = selected_prices.apply(lambda row: row[1]/row[7], axis=1)
    selected_prices['rel_low'] = selected_prices.apply(lambda row: row[2]/row[8], axis=1)
    selected_prices['rel_close'] = selected_prices.apply(lambda row: row[3]/row[9], axis=1)
    selected_prices.plot.line(x='dates', y=['rel_open','rel_high','rel_low','rel_close'])
  else:
    selected_prices.plot.line(x='dates', y=['open','high','low','close'])
  plt.ylim(ymin=0)
  plt.title(symbol)
plt.show()

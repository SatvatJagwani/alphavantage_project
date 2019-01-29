import pandas as pd
import matplotlib.pyplot as plt
import visualize_data
from datetime import datetime
import requests

symbol_list = input("Which symbols to check? (space separated) ").split(' ')
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
  if use_relative_price:
    json_data = requests.get('https://www.alphavantage.co/query?function=SMA&symbol='+symbol+'&interval=daily&time_period=60&series_type=close&apikey=S8VR973UXCO7HEP6').json()
    prices = pd.DataFrame.from_dict(json_data['Technical Analysis: SMA'], orient='index', dtype='float')
  else:
    json_data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey=S8VR973UXCO7HEP6').json()
    prices = pd.DataFrame.from_dict(json_data['Time Series (Daily)'], orient='index', dtype='float')
    prices.columns = ['open', 'high', 'low', 'close', 'volume']
  prices['timestamp'] = prices.index
  prices['dates'] = prices['timestamp'].apply(lambda x: (datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]))-datetime(2018,11,30)).days)
  selected_prices = prices[prices['timestamp'].isin(dates)].set_index('timestamp')
  if use_relative_price:
    selected_prices.plot.line(x='dates', y='SMA')
  else:
    selected_prices.plot.line(x='dates', y=['open','high','low','close'])
  plt.ylim(ymin=0)
  plt.title(symbol)
plt.show()

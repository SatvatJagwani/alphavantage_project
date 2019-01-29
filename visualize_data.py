import pandas as pd
import matplotlib.pyplot as plt

selected_symbols = pd.read_csv('US Stock Symbols - US Stock Symbols.csv')
name_symbol_map = selected_symbols.set_index('Name')['Symbol']

def plot_queries_for_symbols(list_of_symbols=None, function=None, interval=None, ips=None, use_full_stock_name=False):
  stock_query_frequency_series = []
  all_days_top_symbols_set = set()
  everyday_frequencies = {}
  list_of_symbols = list_of_symbols if list_of_symbols else selected_symbols['Symbol'].tolist()
  for i in ['09'] + [str(j) for j in range(10, 23)]:
    df = pd.read_csv('alphavantage_data/2018-12-'+i+'.csv')
    filtered_df = df[df['symbol'].isin(list_of_symbols) & (df['function']==function if function else True) & (df['interval']==interval if interval else True) & (df['ipaddress'].isin(ips) if ips else True)]
    #filtered_df = df[df['symbol'].isin(selected_symbols['Symbol'].tolist()) & (df['ipaddress']==8033523992348097025)]
    everyday_frequencies[i] = filtered_df['symbol'].value_counts()
    top_symbols = everyday_frequencies[i].head(20)
    all_days_top_symbols_set = all_days_top_symbols_set | set(top_symbols.index)
    if use_full_stock_name:
      top_stocks = name_symbol_map.map(top_symbols).dropna().sort_values(ascending=False)
    else:
      top_stocks = top_symbols.dropna().sort_values(ascending=False)
    print(top_stocks)
    #stock_query_frequency_series.append(top_stocks.rename('2018-12-'+i))
  for i in everyday_frequencies.keys():
    day_i_frequency = everyday_frequencies[i]
    top_symbols = day_i_frequency[day_i_frequency.index.isin(all_days_top_symbols_set)]
    stock_query_frequency_series.append(top_symbols.rename('2018-12-'+i))
  frequency_df = pd.concat(stock_query_frequency_series, axis=1).T
  print(frequency_df)
  frequency_df['dates'] = frequency_df.index
  frequency_df['dates'] = frequency_df['dates'].apply(lambda x: int(x[-2:]))
  all_stocks = frequency_df.columns.tolist()
  all_stocks.remove('dates')
  frequency_df.plot.line(x='dates', y=all_stocks, marker='o')

if __name__ == '__main__':
  plot_queries_for_symbols(selected_symbols['Symbol'].tolist(), 'TIME_SERIES_INTRADAY', '60min', {52597408375137639, 70363050222146159, 5491286006367310342, 347841015311346941, 244934347459668734, 787457465656659032, 513221419057790673, 552572711055606718, 946444644988914784, 1004437664065217074, 5175312287075033719, 414604323792544718, 83191216953818442, 5706154976792626252, 7948971321566207268, 2217487475993022600, 7597630797820836567, 442701863205404739, 6284143751848986844, 2051824840058743715, 6581834288311576953, 3838542422459644624, 928583098573582846, 3488953759429449188, 7781126273647843987, 4886837647894589035, 16454890273569039, 5301803874587558213, 4927485626871465910, 7928721173158013710, 3416293872471929474, 3922631177273129, 511879805096109682, 605691566805160798, 105005678973632819, 3667137265361393944, 780286769176028304, 174975026995721397, 2898287971377854675, 26437923933441316, 2076984833703683983, 116833368636468175, 2508483730115791139, 864474852326012641, 142112176165606640, 625740937204609114, 4631033707027971265})
  plt.show()

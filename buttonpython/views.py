from django.shortcuts import render
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import pylab
from matplotlib import pyplot as plt
import plotly.graph_objs as go
import PIL, PIL.Image
from io import BytesIO


def button(request):
    return render(request, 'home.html')

def output(request):
    # request to get candle data from binance api
    BTC = requests.get('https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1m')
    ETH = requests.get('https://api.binance.com/api/v1/klines?symbol=ETHUSDT&interval=1m')
    XRP = requests.get('https://api.binance.com/api/v1/klines?symbol=XRPUSDT&interval=1m')
    BNB = requests.get('https://api.binance.com/api/v1/klines?symbol=BNBUSDT&interval=1m')
    LTC = requests.get('https://api.binance.com/api/v1/klines?symbol=LTCUSDT&interval=1m')
    EOS = requests.get('https://api.binance.com/api/v1/klines?symbol=EOSUSDT&interval=1m')
    TRX = requests.get('https://api.binance.com/api/v1/klines?symbol=TRXUSDT&interval=1m')
    BCH = requests.get('https://api.binance.com/api/v1/klines?symbol=BCHABCUSDT&interval=1m')

    # request to get binance server time
    t = requests.get('https://api.binance.com/api/v1/time')

    # names the various columns from the requested candle data in a dataframe
    BTC_df = pd.DataFrame(BTC.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])
    ETH_df = pd.DataFrame(ETH.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])
    XRP_df = pd.DataFrame(XRP.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])
    BNB_df = pd.DataFrame(BNB.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])
    LTC_df = pd.DataFrame(LTC.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])
    EOS_df = pd.DataFrame(EOS.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])
    TRX_df = pd.DataFrame(TRX.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])
    BCH_df = pd.DataFrame(BCH.json(),
                          columns=['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', '7', '8', '9',
                                   '10', '11'])

    # changes the binance servertime into time that is readable(gregorian time)
    BTC_df['Opentime'] = pd.to_datetime(BTC_df['Opentime'], unit='ms')
    ETH_df['Opentime'] = pd.to_datetime(ETH_df['Opentime'], unit='ms')
    XRP_df['Opentime'] = pd.to_datetime(XRP_df['Opentime'], unit='ms')
    BNB_df['Opentime'] = pd.to_datetime(BNB_df['Opentime'], unit='ms')
    LTC_df['Opentime'] = pd.to_datetime(LTC_df['Opentime'], unit='ms')
    EOS_df['Opentime'] = pd.to_datetime(EOS_df['Opentime'], unit='ms')
    TRX_df['Opentime'] = pd.to_datetime(TRX_df['Opentime'], unit='ms')
    BCH_df['Opentime'] = pd.to_datetime(BCH_df['Opentime'], unit='ms')

    # makes the 'opentime' of the first column each dataframe as the index
    BTC_df.set_index('Opentime', inplace=True)
    ETH_df.set_index('Opentime', inplace=True)
    XRP_df.set_index('Opentime', inplace=True)
    BNB_df.set_index('Opentime', inplace=True)
    LTC_df.set_index('Opentime', inplace=True)
    EOS_df.set_index('Opentime', inplace=True)
    TRX_df.set_index('Opentime', inplace=True)
    BCH_df.set_index('Opentime', inplace=True)

    # droppnig unnecessary columns
    BTC_df = BTC_df.drop(['Closetime', '11'], axis=1)
    ETH_df = ETH_df.drop(['Closetime', '11'], axis=1)
    XRP_df = XRP_df.drop(['Closetime', '11'], axis=1)
    BNB_df = BNB_df.drop(['Closetime', '11'], axis=1)
    LTC_df = LTC_df.drop(['Closetime', '11'], axis=1)
    EOS_df = EOS_df.drop(['Closetime', '11'], axis=1)
    TRX_df = TRX_df.drop(['Closetime', '11'], axis=1)
    BCH_df = BCH_df.drop(['Closetime', '11'], axis=1)

    # converts entire dataframe from object to float and integer
    BTC_df = BTC_df.apply(pd.to_numeric)
    ETH_df = ETH_df.apply(pd.to_numeric)
    XRP_df = XRP_df.apply(pd.to_numeric)
    BNB_df = BNB_df.apply(pd.to_numeric)
    LTC_df = LTC_df.apply(pd.to_numeric)
    EOS_df = EOS_df.apply(pd.to_numeric)
    TRX_df = TRX_df.apply(pd.to_numeric)
    BCH_df = BCH_df.apply(pd.to_numeric)

    # concatenation of the 'close' price columns into one
    data1 = pd.concat(
        [BTC_df['Close'], ETH_df['Close'], XRP_df['Close'], BNB_df['Close'], LTC_df['Close'], EOS_df['Close'],
         TRX_df['Close'], BCH_df['Close']], axis=1)
    # naming of the columns in the new panda dataframe named 'data'
    data1.columns = ['BTC', 'ETH', 'XRP', 'BNB', 'LTC', 'EOS', 'TRX', 'BCH']

    # normalizes the dataframes
    BTC_df = (BTC_df - BTC_df.mean()) / (BTC_df.max() - BTC_df.min())
    ETH_df = (ETH_df - ETH_df.mean()) / (ETH_df.max() - ETH_df.min())
    XRP_df = (XRP_df - XRP_df.mean()) / (XRP_df.max() - XRP_df.min())
    BNB_df = (BNB_df - BNB_df.mean()) / (BNB_df.max() - BNB_df.min())
    LTC_df = (LTC_df - LTC_df.mean()) / (LTC_df.max() - LTC_df.min())
    EOS_df = (EOS_df - EOS_df.mean()) / (EOS_df.max() - EOS_df.min())
    TRX_df = (TRX_df - TRX_df.mean()) / (TRX_df.max() - TRX_df.min())
    BCH_df = (BCH_df - BCH_df.mean()) / (BCH_df.max() - BCH_df.min())

    # concatenation of the 'close' price columns into one
    data2 = pd.concat(
        [BTC_df['Close'], ETH_df['Close'], XRP_df['Close'], BNB_df['Close'], LTC_df['Close'], EOS_df['Close'],
         TRX_df['Close'], BCH_df['Close']], axis=1)
    # naming of the columns in the new panda dataframe named 'data'
    data2.columns = ['BTC', 'ETH', 'XRP', 'BNB', 'LTC', 'EOS', 'TRX', 'BCH']
    coin_name = ['BTC', 'ETH', 'XRP', 'BNB', 'LTC', 'EOS', 'TRX', 'BCH']

    data = data2.corr()
    plt.figure(figsize=(19,16))
    matrix = sns.heatmap(data,
                         cmap='YlGnBu',
                         annot=True,
                         annot_kws={'size': 15},
                         vmin=0,
                         vmax=1,
                         linewidths=0.5,
                         square=True,
                         fmt="0.4")

    matrix.set_xticklabels(matrix.get_xticklabels(),
                           horizontalalignment='center',
                           fontsize='15')

    matrix.set_yticklabels(matrix.get_yticklabels(),
                           verticalalignment='center',
                           rotation=0,
                           fontsize='15')
    matrix.xaxis.set_ticks_position('top')
    #matrix.set_title('Correlation of Cryptocurrencies', fontsize=28)
    # plt.show()
    plt.savefig('https://127.0.0.1:8001/matrix.png')

    data = coin_name
    return render(request, 'home.html', {'data':data})

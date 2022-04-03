import pandas as pd
import numpy as np
import datetime as dt
import pandas_datareader as pdr
import seaborn as sns
import matplotlib.pyplot as plt
from ib_insync import *
from utils import Wilder
import eel


class DataStock():
    def __init__(self,tickers,data=None,period=5):
        self.tickers = tickers
        self.all_data = pd.DataFrame()
        self.test_data = pd.DataFrame()
        self.period = 5
        #self.ib = IB()
        #self.ib.connect('127.0.0.1', 7496, clientId=1,readonly=True)
        
    def create_test_data(self):
        print(dt.date.today())
        no_data = []
        for i in self.tickers:
            try:
                test_data = pdr.get_data_yahoo(i, start = dt.datetime(1990,1,1), end = dt.date.today())
                test_data['symbol'] = i
                self.all_data = self.all_data.append(test_data)
            except:
                no_data.append(i)
        self.all_data['return'] = self.all_data.groupby('symbol')['Close'].pct_change() 
        print(*no_data)


    def update_indicators(self,data):
        self.calc_sma()
        self.calc_dm()
        #TODO new to add new data to existing data

    def update_data(self):
        contract = Stock(*self.tickers) #Stock('AMD','Tesla',...)
        #TODO replace below with live values instead of historical
        bars = self.ib.reqHistoricalData(
        contract, endDateTime='', durationStr='30 D',
        barSizeSetting='1 hour', whatToShow='HISTORICAL_VOLATILITY', useRTH=True)
        df = util.df(bars)
        #TODO replace original dataframe or append to it (care memory overflow)
        self.all_data += df #example

    def update_tickers(self):
        self.tickers = eel.request_data_js("stock_symbols")


    def update(self):
        self.update_tickers()
        self.update_data() 
        self.calc_sma()
        self.calc_dm()
        self.check_all_dm_crossing()
        #trigger crossing event

    def calc_sma(self,period):
        self.all_data['SMA_'+str(period)] = self.all_data.groupby('symbol')['Close'].transform(lambda x: x.rolling(window = period).mean())

    def calc_dm(self,period):
        self.all_data['prev_close'] = self.all_data.groupby('symbol')['Close'].shift(1)
        self.all_data['TR'] = np.maximum((self.all_data['High'] - self.all_data['Low']), 
                            np.maximum(abs(self.all_data['High'] - self.all_data['prev_close']), 
                            abs(self.all_data['prev_close'] - self.all_data['Low'])))
        for i in self.all_data['symbol'].unique():
            TR_data = self.all_data[self.all_data.symbol == i].copy()
            self.all_data.loc[self.all_data.symbol==i,'ATR_'+str(period)] = Wilder(TR_data['TR'], period)

        self.all_data['prev_high'] = self.all_data.groupby('symbol')['High'].shift(1)
        self.all_data['prev_low'] = self.all_data.groupby('symbol')['Low'].shift(1)

        self.all_data['+DM'] = np.where(~np.isnan(self.all_data.prev_high),
                                np.where((self.all_data['High'] > self.all_data['prev_high']) & 
                (((self.all_data['High'] - self.all_data['prev_high']) > (self.all_data['prev_low'] - self.all_data['Low']))), 
                                                                        self.all_data['High'] - self.all_data['prev_high'], 
                                                                        0),np.nan)

        self.all_data['-DM'] = np.where(~np.isnan(self.all_data.prev_low),
                                np.where((self.all_data['prev_low'] > self.all_data['Low']) & 
                (((self.all_data['prev_low'] - self.all_data['Low']) > (self.all_data['High'] - self.all_data['prev_high']))), 
                                            self.all_data['prev_low'] - self.all_data['Low'], 
                                            0),np.nan)

        for i in self.all_data['symbol'].unique():
            ADX_data = self.all_data[self.all_data.symbol == i].copy()
            self.all_data.loc[self.all_data.symbol==i,'+DM_'+str(period)] = Wilder(ADX_data['+DM'], period)
            self.all_data.loc[self.all_data.symbol==i,'-DM_'+str(period)] = Wilder(ADX_data['-DM'], period)

        self.all_data['+DI_'+str(period)] = (self.all_data['+DM_'+str(period)]/self.all_data['ATR_'+str(period)])*100
        self.all_data['-DI_'+str(period)] = (self.all_data['-DM_'+str(period)]/self.all_data['ATR_'+str(period)])*100

        self.all_data['DX_'+str(period)] = (np.round(abs(self.all_data['+DI_'+str(period)] - self.all_data['-DI_'+str(period)])/(self.all_data['+DI_'+str(period)] + self.all_data['-DI_'+str(period)]) * 100))


        for i in self.all_data['symbol'].unique():
            ADX_data = self.all_data[self.all_data.symbol == i].copy()
            self.all_data.loc[self.all_data.symbol==i,'ADX_'+str(period)] = Wilder(ADX_data['DX_'+str(period)], period)
    
    def check_all_dm_crossing(self,period):
        #check value crossing for entire data depth
        mask = (self.all_data['+DI_'+str(period)].shift().lt(self.all_data['-DI_'+str(period)]) & self.all_data['+DI_'+str(period)].ge(self.all_data['-DI_'+str(period)])) | (self.all_data['-DI_'+str(period)].shift().lt(self.all_data['+DI_'+str(period)]) & self.all_data['-DI_'+str(period)].ge(self.all_data['+DI_'+str(period)]))
        self.all_data['+DI_'+str(period)+'_cross_'+'DI_'+str(period)] = mask
        idx = self.all_data['+DI_'+str(period)+'_cross_'+'DI_'+str(period)].index.tolist()
        #TODO Trigger Event/Alert python/javascript if new crossing detected
        
        return idx

    def plot_sma(self,symbol,period):
        start = dt.datetime.strptime('2019-01-01', '%Y-%m-%d')
        end = dt.datetime.strptime('2019-12-31', '%Y-%m-%d')
        sns.set()

        fig = plt.figure(facecolor = 'white', figsize = (20,10))

        ax0 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
        ax0.plot(self.all_data[self.all_data.symbol==symbol].loc[start:end,['Close','SMA_'+str(period)]])
        ax0.set_facecolor('ghostwhite')
        ax0.legend(['Close','SMA_'+str(period)],ncol=3, loc = 'upper left', fontsize = 15)
        plt.title(symbol+" Moving Average in Period: "+str(period), fontsize = 20)

        #plt.subplots_adjust(left=.09, bottom=.09, right=1, top=.95, wspace=.20, hspace=0)
        plt.show()
        input() #TODO remove this once testing not nec. anymore
        


    def plot_dm(self,symbol,period):
        #Plotting
        start = dt.datetime.strptime('2019-01-01', '%Y-%m-%d')
        end = dt.datetime.strptime('2019-12-31', '%Y-%m-%d')
        sns.set()

        fig = plt.figure(facecolor = 'white', figsize = (20,10))

        ax0 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
        ax0.plot(self.all_data[self.all_data.symbol==symbol].loc[start:end,['Close']])
        ax0.set_facecolor('ghostwhite')
        ax0.legend(['Close'],ncol=3, loc = 'upper left', fontsize = 15)
        plt.title(symbol+" Stock Price ADX, DI+ and DI- in Period: "+ str(period), fontsize = 20)

        ax1 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = ax0)
        ax1.plot(self.all_data[self.all_data.symbol==symbol].loc[start:end,['ADX_'+str(period)]], color = 'orange')
        ax1.plot(self.all_data[self.all_data.symbol==symbol].loc[start:end,['+DI_'+str(period)]], color = 'blue')
        ax1.plot(self.all_data[self.all_data.symbol==symbol].loc[start:end,['-DI_'+str(period)]], color = 'red')

        ax1.legend(['ADX_'+str(period),'+DI_'+str(period),'-DI_'+str(period)],ncol=3, loc = 'upper left', fontsize = 12)
        ax1.set_facecolor('silver')
        plt.subplots_adjust(left=.09, bottom=.09, right=1, top=.95, wspace=.20, hspace=0)
        plt.show()
        input() #TODO remove this once testing not nec. anymore


if __name__ == '__main__':

    #extracting data from Yahoo Finance API
    tickers = ['AAPL','NFLX']
    data_stock = DataStock(tickers)
    data_stock.create_test_data()
    period = 10
    #data_stock.calc_sma(period)
    #data_stock.plot_sma('AAPL',period)
    data_stock.calc_dm(period)
    data_stock.plot_dm('AAPL',period)
    data_stock.check_all_dm_crossing(period)




    
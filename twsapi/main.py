import threading
import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from matplotlib import pyplot as plt


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')

    def tickSize(self, reqId, tickType, size):
        print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.impliedVola = []
        self.ask = []
        self.histVola = []

    def historicalData(self, reqId, bar):
        if reqId == 1:
            self.impliedVola.append([bar.date, bar.close])
        if reqId == 2:
            self.ask.append([bar.date, bar.close])
        if reqId == 3:
            self.histVola.append([bar.date, bar.close])


def run_loop():
    app.run()

app = IBapi()
app.connect("127.0.0.1", 7497, 0)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)

var1_contract = Contract()
var1_contract.symbol = 'TSLA'
var1_contract.secType = 'STK'
var1_contract.currency = 'USD'
var1_contract.exchange = 'SMART'

app.reqHistoricalData(1, var1_contract, '', '8 y', '1 day', 'OPTION_IMPLIED_VOLATILITY', 0, 1, False, [])
app.reqHistoricalData(2, var1_contract, '', '8 y', '1 day', 'ASK', 0, 1, False, [])
app.reqHistoricalData(3, var1_contract, '', '8 y', '1 day', 'HISTORICAL_VOLATILITY', 0, 1, False, [])

time.sleep(5)

import pandas

df = pandas.DataFrame(app.impliedVola, columns=['DataTime', 'Implied Vola'])
dfHistVola = pandas.DataFrame(app.histVola, columns=['DataTime', 'Hist Vola'])
dfAsk = pandas.DataFrame(app.ask, columns=['DataTime', 'Ask'])

df['Hist Vola']=dfHistVola['Hist Vola']
df['Ask']=dfAsk['Ask']

df.head(10)

df.plot()
plt.show()

df.to_csv('data.csv')

print(df)


def main():
    '''app = TestApp()

    app.connect("127.0.0.1", 7497, 0)

    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"

    app.reqMarketDataType(4)  # switch to delayed-frozen data if live is not available
    app.reqMktData(1, contract, "", False, False, [])

    app.run()'''


if __name__ == "__main__":
    main()
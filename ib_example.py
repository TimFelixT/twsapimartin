from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1,readonly=True)

contract = Stock('AMD','SMART','USD')
bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='HISTORICAL_VOLATILITY', useRTH=True)

# convert to pandas dataframe:
df = util.df(bars)
print(df)
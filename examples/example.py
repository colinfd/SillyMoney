import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt
import pickle

symbol = "DDD"
start = datetime.date(2010,1,1)
end = datetime.date(2017,1,16)

stock = pdr.DataReader(symbol,"google",start,end)
pickle.dump(stock,open('AAPL.pkl','w'))

stock2 = pdr.DataReader("A","google",start,end)
pickle.dump(stock2,open('A.pkl','w'))

stock3 = pdr.DataReader("A","yahoo",start,end)

stock['Open'].plot()

reader = pdr.google.daily.GoogleDailyReader(symbol,start,end)

plt.show()

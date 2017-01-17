import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt
import pickle

symbol = "AAPL"
start = datetime.datetime(2010,1,1)
end = datetime.date.today()

stock = pdr.DataReader(symbol,"google",start,end)
pickle.dump(stock,open('AAPL.pkl','w'))

stock['Open'].plot()

reader = pdr.google.daily.GoogleDailyReader(symbol,start,end)

plt.show()

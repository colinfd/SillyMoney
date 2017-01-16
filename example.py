import pandas_datareader as pdr
import datetime
import matplotlib.pyplot as plt

index = "AAPL"
start = datetime.datetime(2016,1,1)
end = datetime.date.today()

stock = pdr.DataReader(index,"google",start,end)

stock['Open'].plot()
plt.show()

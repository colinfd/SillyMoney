import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pickle
import glob
import random
import numpy as np

#TO-DO:
#Print summary of trades in command line
#   Average net %, investment duration, average yearly net %
#Add % to secondary y-axis

stock_pkls = glob.glob('../data/*.pkl')
random.shuffle(stock_pkls)

ex_stock = pickle.load(open('../examples/A.pkl'))
dates = ex_stock.index.values
n_dates = 100
pt = 0 #open, close, high, low, volume

class Broker():
    def __init__(self):
        self.stock_ctr = 0
        self.net_percents = []
        self.invest_durs = []

        self.fig, self.ax = plt.subplots()
        self.plot = self.ax.plot(ex_stock.index.values,ex_stock['Open'])[0]
        
        axbuy = plt.axes([0.15, 0.80, 0.1, 0.12])
        axsell = plt.axes([0.15, 0.70, 0.1, 0.12])
        axadv = plt.axes([0.15, 0.60, 0.2, 0.12])
        bbuy = Button(axbuy, 'Buy')
        bbuy.on_clicked(self.buy)
        bsell = Button(axsell, 'Sell')
        bsell.on_clicked(self.sell)
        badv = Button(axadv, 'Advance')
        badv.on_clicked(self.advance)

        self.new_stock()

    def buy(self,event):
        price = float(self.stock[self.day_index][pt])
        self.spent += price
        self.n_current_stock += 1
        print "Bought stock in %s for %.2f"%(self.stock_sym,price)
        self.purchase = (self.day_index - self.start_index,price)

        self.advance()

    def sell(self,event):
        #Record profits and investment duration
        if self.spent == 0:
            self.new_stock()

        self.net_percents.append((self.n_current_stock*float(self.stock[self.day_index][pt]) - self.spent)/self.spent * 100)
        self.invest_durs.append(self.day_index-self.start_index)
        
        #Start new stock
        self.new_stock()

    def advance(self,*args):
        self.day_index += 1
        if self.stock[self.day_index][pt] == 'N/A':
            if self.day_index < len(self.stock):
                self.advance()
            else:
                self.new_stock()
        self.draw()
    
    def draw(self):
        #Update x and y data for stocks
        #self.plot.set_xdata(dates[self.start_index:self.day_index])
        self.plot.set_xdata(range(self.day_index-self.start_index))
        ydata = [i[pt] for i in self.stock[self.start_index:self.day_index]]
        for i,dat in enumerate(ydata):
            if dat == 'N/A':
                ydata[i] = np.nan
        self.plot.set_ydata(ydata)
        
        #Update position of purchases
        if self.purchase is not None:
            self.ax.plot(self.purchase[0],self.purchase[1],'ro')

        self.ax.set_title("%s (%s)"%(self.stock_name,self.stock_sym))
        self.ax.relim()
        self.ax.autoscale_view()

        if self.stock_ctr == 1: #first stock
            plt.show()

    def new_stock(self):
        #Pick a new stock at random
        f = open(stock_pkls[self.stock_ctr])
        self.stock = pickle.load(f)
        f.close()
        self.stock_sym = self.stock['meta']['sym']
        self.stock_name = self.stock['meta']['name']
        self.stock = self.stock['data']

        self.n_current_stock = 0
        self.spent = 0
        self.purchase = None

        #Pick a start date at random
        self.start_index = random.randint(0,len(dates)-n_dates-100) #allow for at least 100 days of trading
        self.day_index = self.start_index + n_dates #index of current day

        self.stock_ctr += 1
        self.advance()
        self.draw()

Broker()

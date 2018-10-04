import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pickle
import glob
import random
import numpy as np

class Broker():
    def __init__(self,price_type='open',n_dates=250,scalar_analyses=[],vector_analyses=[]):
        """
        Broker class that keeps track of stock prices and purchases and updates the active window.

        price_type: one of 'open','close','high','low'
            value of stock to consider on each day

        n_dates: number of previous trading days shown to user

        scalar_analyses: list of functions of the type vector --> scalar
            every trading day, each function will be evaluated with the up-to-date stock data and
            the result is printed to the user

        vector_analyses: list of functions of the type vector --> vector
            every trading day, each function will be evaluated with the up-to-date stock data and
            the result is overlayed on the stock data

        """
        if price_type not in ['open','close','high','low']:
            raise InputError("price_type must be one of 'open','close','high','low'")
        else:
            self.pt = {'open':0, 'close':1, 'high':2, 'low':3}[price_type]

        self.n_dates = n_dates
        self.scalar_analyses = scalar_analyses #list of scalar functions to analyze on each day with each stock, use self.attach_scalar_analysis()
        self.vector_analyses = vector_analyses
        
        self.stock_ctr = 0 #number of stocks seen this session
        self.dates = range(1771) #list of all trading days
        self.mean_daily_percents = [] #percentage gains on each stock seen this session

        self.stock_csvs = glob.glob('../data/*.csv')
        random.shuffle(self.stock_csvs)
        
        #Initialize interactive window with stock data
        self.fig, self.ax = plt.subplots() #figure used for plotting stock info
        self.ax2 = self.ax.twinx()
        self.plot = self.ax.plot([0,1],[0,1])[0]#Line2D object corresponding to stock price
        self.purchase_plot = self.ax.plot(np.nan,np.nan,'ro',markersize=6)[0]#Line2D object corresponding to purchases
        self.purchase_mean_plot = self.ax.plot(np.nan,np.nan,'--r',lw=1)[0]#Line2D object corresponding to purchase mean

        self.analyses_plots = []
        for vector_analysis in vector_analyses:
            self.analyses_plots.append(self.ax.plot(np.nan,np.nan,'-k',linewidth=1.5)[0])
            
        
        #Define buttons for user control
        axbuy = plt.axes([0.15, 0.80, 0.1, 0.12]) #buy
        bbuy = Button(axbuy, 'Buy')
        bbuy.on_clicked(self.buy)
        axsell = plt.axes([0.15, 0.70, 0.1, 0.12]) #sell
        bsell = Button(axsell, 'Sell')
        bsell.on_clicked(self.sell)
        axadv = plt.axes([0.15, 0.60, 0.2, 0.12]) #advance to next day without activity
        badv = Button(axadv, 'Advance')
        badv.on_clicked(self.advance)
        
        self.new_stock()

    def new_stock(self):
        #Pick a new stock at random
        fname = self.stock_csvs[self.stock_ctr]
        """
        f = open(fname)
        self.stock = pickle.load(f)
        f.close()
        self.stock_sym = self.stock['meta']['sym']
        self.stock_name = self.stock['meta']['name']
        self.stock = self.stock['data'] #list of lists containing open, close, high, low for each market day
        """
        self.stock, self.stock_meta = self.load_stock(fname)

        self.purchases = [] #to be populated with [purchase price, purchase date (relative to self.start_index)]

        #Pick a start date at random
        self.start_index = random.randint(0,len(self.dates)-self.n_dates-100) #allow for at least 100 days of trading
        self.day_index = self.start_index + self.n_dates #index of current day

        self.stock_ctr += 1
        self.advance() #makes sure that stock has data on first day
        self.ax.set_autoscale_on(True)
        self.draw() #update chart
    
    def load_stock(self,fname):
        f = open(fname)
        lines = f.readlines()
        f.close()
        meta = lines[0].strip().split(',')
        meta = {'sym':meta[0],'name':meta[1],'exchange':meta[2]}

        data = []

        for i in range(1,len(lines)):
            data += [lines[i].strip().split(',')]

        #data = np.loadtxt(fname,skiprows=1,delimiter=',')#,converters={'N/A':np.nan})

        return data,meta



    def draw(self):
        #Update x and y data for stocks
        self.plot.set_xdata(range(self.day_index-self.start_index+1))
        ydata = [i[self.pt] for i in self.stock[self.start_index:self.day_index+1]]
        for i,dat in enumerate(ydata):
            if dat == 'N/A':
                ydata[i] = np.nan
            else:
                ydata[i] = float(ydata[i])
        self.plot.set_ydata(ydata)
        self.ax.relim()
        self.ax.autoscale_view()

        #update 2nd y-axis which shows percentage change relative stock price
        self.ax2.set_ylim(np.array(self.ax.get_ylim())/ydata[-1]*100-100)
        labels = []
        for tick in self.ax2.get_yticks():
            label = str(tick)
            if tick >= 0:
                label = '+' + label
            label += '%'
            labels.append(label)
        self.ax2.set_yticklabels(labels)


        #Run scalar analyses and add to title
        title = ""
        for fun in self.scalar_analyses:
            title += "%s = %.2f"%(fun.__name__,fun(ydata))
        self.plot.axes.set_title(title)

        #Run vector analyses and add to plot
        for i,fun in enumerate(self.vector_analyses):
            self.analyses_plots[i].set_xdata(range(self.day_index-self.start_index+1))
            self.analyses_plots[i].set_ydata(fun(ydata))
            
        
        #Update position of purchases
        if len(self.purchases) > 0:
            purch_prices,purch_days = zip(*self.purchases)
            self.purchase_plot.set_xdata(purch_days)
            self.purchase_plot.set_ydata(purch_prices)

            #Update average purchase price
            if len(self.purchases) > 0:
                pmp = self.purchase_mean_plot
                xlim = pmp.axes.get_xlim()
                pmp.set_xdata(xlim)
                pmp.set_ydata([np.mean(purch_prices)]*2)

                
        if self.stock_ctr == 1: #first stock
            plt.show()

    def advance(self,*args):
        #advance to next day with stock data available
        self.day_index += 1
        if self.stock[self.day_index][self.pt] == 'N/A':
            if self.day_index < len(self.stock):
                try:
                    self.advance()
                    return
                except RuntimeError:
                    self.new_stock()
            else:
                self.new_stock()
        self.draw()

    def buy(self,event):
        #purchase stock on current day

        price = float(self.stock[self.day_index][self.pt])
        day = self.day_index - self.start_index
        self.purchases.append([price,day])

        print "Bought stock in %s for %.2f"%(self.stock_meta['sym'],price)

        self.advance() #only allow one purchase per day
        
    def sell(self,event):
        #Record profits and investment duration
        if len(self.purchases) > 0:
            sell_price = float(self.stock[self.day_index][self.pt])
            
            #calculate return on investment
            purchase_prices = np.array([i[0] for i in self.purchases])
            purchase_dates = np.array([i[1] for i in self.purchases])
            #mean_daily_percent = np.mean((sell_price - purchase_prices)/purchase_prices/(self.day_index-self.start_index-purchase_dates))*100 #mean assuming all independent trades, more relevant for a pure algorithm
            mean_daily_percent = (sell_price - purchase_prices.mean())/purchase_prices.mean()/len(purchase_prices)*100 #mean over the current stock
            self.mean_daily_percents.append((mean_daily_percent,self.day_index-self.start_index-purchase_dates[0]))
            total_days = sum([i[1] for i in self.mean_daily_percents])
            total_mean = sum([i[0]*i[1]/total_days for i in self.mean_daily_percents])
            
            print "="*15
            print "Sold %d shares of %s for $%.2f/share"%(len(self.purchases),self.stock_meta['sym'],sell_price)
            print "Mean daily percentage return = %.2f%%/day"%mean_daily_percent
            print "="*15
            print "Current Session: Averaging %.2f%%/day on %d stocks over %d total days\n"%(total_mean,len(self.mean_daily_percents),total_days)
            
        #Start new stock
        self.new_stock()

def slope_sign_change(prices):
    #return percentage of days that have change in first derivative
    changes = 0
    #remove nan from prices
    indices = [i for i in range(len(prices)) if prices[i] == np.nan]
    np.delete(prices,indices)

    delta = prices[1] - prices[0]
    if delta > 0:
        d = 'up'
    else:
        d = 'down'

    for i in range(len(prices) - 2):
        delta = prices[i+2] - prices[i+1]
        
        if delta > 0:
            if d == 'down':
                changes += 1
                d = 'up'
        else:
            if d == 'up':
                changes += 1
                d = 'down'

    return float(changes)/float(len(prices)-1)

def rms_disp(prices):
    #return rms_disp of stock from running_mean
    prices = np.array(prices)
    means = np.array(running_mean(prices))
    rms = np.sqrt(np.mean(((prices-means)/means)**2))*100
    return rms

def running_mean(prices):
    out = []
    n = 5
    for i,p in enumerate(prices):
        if i < n:
            out.append(np.mean(prices[:i+n+1]))
        elif i > len(prices) - n:
            out.append(np.mean(prices[i-n:]))
        else:
            out.append(np.mean(prices[i-n:i+n+1]))

    return out

def running_mean(prices,n=3):
    ret = np.cumsum(prices, dtype=np.float16)
    ret[n:] = ret[n:] - ret[:-n]
    for i in range(n-1): ret = np.insert(ret,0,ret[n-1])
    return ret[n - 1:] / n

    out = np.zeros(len(prices),dtype=np.float16)
    n = 5
    for i,p in enumerate(prices):
        if i < n:
            out[i] = np.mean(prices[:i+n+1])
        elif i > len(prices) - n:
            out[i] = np.mean(prices[i-n:])
        else:
            out[i] = np.mean(prices[i-n:i+n+1])

    return out


b = Broker(scalar_analyses = [rms_disp])
#b = Broker(scalar_analyses = [rms_disp],vector_analyses = [running_mean])

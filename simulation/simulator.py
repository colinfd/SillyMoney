import pickle
import glob
import numpy as np
import random

class Simulator():
    """
    Automatic simulator that manages cash flows and makes stock decisions based on 3 user-defined functions:
    val_fun, buy_fun, and sell_fun
    """
    def __init__(self,sim_length,cash,val_fun,buy_fun,sell_fun,n_stocks=None,verbose=False,buy_pt='open',sell_pt='open',dates=None,exclude_list=[],daily_limit = 1e10,data_path=None):
        self.sim_length = sim_length #days
        self.start_cash = cash #dollars
        self.val_fun = val_fun
        self.buy_fun = buy_fun
        self.sell_fun = sell_fun
        self.verbose= verbose
        self.buy_pt = buy_pt
        self.sell_pt = sell_pt
        self.daily_limit = daily_limit
        
        if dates is None:
            self.dates = [str(date).split('T')[0] for date in pickle.load(open('/home/colinfd/silly_money/examples/A.pkl')).index.values] #1771 dates for market trading
        else:
            self.dates = dates
       
        if data_path is None:
            self.data_path = '/home/colinfd/silly_money/data/'
        else:
            self.data_path = data_path
        
        self.stock_names = []
        for stock_pkl in glob.glob(self.data_path + '*.pkl'):
            stock_name = stock_pkl.split('/')[-1][:-4]
            if stock_name not in exclude_list:
                self.stock_names.append(stock_name)
        if n_stocks is not None: self.stock_names = self.stock_names[:n_stocks+1]

        self.stock_data = {}
    
    def cleanup(self):
        """
        Reset important variables between runs
        """
        self.start_ind = random.randint(0,len(self.dates)-self.sim_length) #starting point
        self.cash = self.start_cash
        self.logfile = "%s.log"%self.dates[self.start_ind]
        if len(glob.glob(self.logfile)) > 0: #this date has already run
            self.cleanup()
        else:
            self.held_stocks = {}
            for stock_name in self.stock_names:
                    self.held_stocks[stock_name] = 0
            
            self.buy_market_prices = {}

    def run(self):
        self.cleanup()
        f = open(self.logfile,'a')
        prev_cash = 1e10
        for day_ind in range(self.start_ind,self.start_ind+self.sim_length):
            self.day_ind = day_ind
            
            #create dictionary of current market prices
            for i,stock_name in enumerate(self.stock_names):
                self.buy_market_prices[stock_name] = self.market_price(stock_name,self.buy_pt)
                            
            #start logging
            log = "%s\nCash: %.2f\nHeld: %s\n"%(self.dates[day_ind],self.cash,self.stock_string(self.held_stocks,pt='open')) #start log of new day
            
            #use functions to determine activity for the day
            val_dict = {}
            for stock_name in self.stock_names:
                val_dict[stock_name] = self.val_fun(stock_name)
            
            sell_dict = self.sell_fun(val_dict,self.held_stocks)
            for stock_name in sell_dict:
                self.held_stocks[stock_name] -= sell_dict[stock_name]
                assert self.held_stocks[stock_name] >= 0 ,"Bad sell_fun ... NEGATIVE STOCKS!"
                self.cash += sell_dict[stock_name]*self.market_price(stock_name,self.sell_pt)
            
            if self.cash/prev_cash > self.daily_limit: #exceeded maximum daily increase...avoid non-physical gains
                self.cash = prev_cash
            else:
                prev_cash = self.cash
            
            log += "Value: %.2f\n"%self.cash
            
            buy_dict = self.buy_fun(val_dict,self.cash,self.buy_market_prices)
            for stock_name in buy_dict:
                self.held_stocks[stock_name] += buy_dict[stock_name]
                self.cash -= buy_dict[stock_name]*self.buy_market_prices[stock_name]
                assert self.cash > 0, "Bad buy_fun ... NEGATIVE CASH!"

            log += "Sales: %s\n"%self.stock_string(sell_dict,self.sell_pt)
            log += "Purchases: %s\n\n"%self.stock_string(buy_dict,self.buy_pt)
            if self.verbose: print log

            f.write(log)
        print "Run finished"
        f.close()

    def market_price(self,stock_name,pt):
        i = -1
        prices = self.read_stock(stock_name,start_i=0,end_i=self.day_ind+1,pt=pt)
        while True:
            if "%s"%prices[i] == 'nan':
                if i == -len(prices):
                    return 1e10 #stock has no history yet, do not allow purchase
                else:
                    i -= 1
            else:
                assert type(prices[i]) == np.float16
                return prices[i]

    def stock_string(self,dict,pt):
        """
        Take stock dict (stock name keys with int values) and return string as "GOOGx4@122.54 ..." using current market prices
        """
        out = ""
        keys = dict.keys()
        for stock_name in dict:
            if dict[stock_name] > 0:
                out += "%sx%s@%.2f "%(stock_name,dict[stock_name],self.market_price(stock_name,pt))
        return out

    def total_value(self,held_stocks):
        """
        DEPRECATED
        Take stock dict and return value at current market price
        """
        if len(held_stocks) == 0:
            return 0
        total = sum([self.market_price(stock_name,self.sell_pt)*held_stocks[stock_name] for stock_name in held_stocks if held_stocks[stock_name] > 0]) 
        return total

    def read_stock(self,stock_name,start_i=0,end_i=None,pt='open',prev_day=False):
        """
        Return numpy array of slice of stock_data from start_i to end_i
        pt = 'open', 'close', 'high', 'low', 'volume'
        When used for first time, will create self.stock_data dictionary with pt keys, stock_name keys and np.array price history as values
        """
        pt_dict = {'open':0,'close':1,'high':2,'low':3,'volume':4}
        if pt not in self.stock_data:
            self.stock_data[pt] = {}
            for stock in self.stock_names:
                f = open(self.data_path + stock + '.pkl')
                stock_dict = pickle.load(f)
                f.close()
                self.stock_data[pt][stock] = np.zeros(len(self.dates),dtype=np.float16)
                for d in range(len(self.dates)):
                    price = stock_dict['data'][d][pt_dict[pt]]
                    if price == 'N/A' or price == 'nan':
                        self.stock_data[pt][stock][d] = np.nan
                    else:
                        self.stock_data[pt][stock][d] = price
        
        if end_i == None:
            end_i = self.day_ind + 1
        if prev_day:
            end_i -= 1

        return self.stock_data[pt][stock_name][start_i:end_i]

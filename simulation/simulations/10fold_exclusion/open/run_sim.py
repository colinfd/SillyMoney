from simulation import Simulator
import numpy as np
from simulation.funs import running_mean,mean_disp #optimized functions for analyzing stock data

##############################################
#FUNCTIONS FOR USE IN SIMULATOR
##############################################
def val(stock_name):
    """
    Take the name of a stock and return a scalar that is used to evaluate its investment value.
    sim.read_stock(stock_name) returns stock data up to the current day
    """
    prices = sim.read_stock(stock_name,pt='open')
    diff = [prices[-2] - prices[-3], prices[-1] - prices[-2]]
    if diff[1] < 0 and diff[1] > diff[0]:
        return (diff[1] - diff[0])/prices[-1]
    else:
        return 0

def sell(val_dict, held_stocks):
    """
    val_dict and held_stocks are both dictionaries containing stock name keys and scalar values.
    scalars in val_dict correspond to val(stock_name) and scalars in held_stocks correspond to
    number of stocks currently owned.

    return a dictionary with stock name keys and int values which determine which stocks to sell.
    """
    sell_dict = {}
    
    for stock_name in held_stocks:
        if held_stocks[stock_name] > 0:
            sell_dict[stock_name] = held_stocks[stock_name]
    
    return sell_dict

def buy(val_dict,cash,market_prices):
    """
    val_dict and market_prices are both dictionaries containing stock name keys and scalar values.
    scalars in val_dict correspond to val(stock_name) and scalars in held_stocks correspond to
    current markey price of stock. 
    cash is the current cash in posession.

    return a dictionary with stock name keys and int values which determine which stocks to buy.
    sum([out[stock]*market_prices[stock] for stock in out]) < cash
    """
    buy_dict = {}

    n = n_buy
    vals = [(stock_name,val_dict[stock_name]) for stock_name in val_dict]
    vals = sorted(vals,key = lambda x : x[1],reverse=True)
    
    for i in range(n):
        try:
            buy_dict[vals[i][0]] = int(cash/n/market_prices[vals[i][0]])
        except:
            print vals[i],market_prices[vals[i][0]]
    
    return buy_dict


##############################################i
#RUN SIMULATOR
##############################################
exclude_list = ['FPAY','FNCX','CIDM']
n_buy = 5

sim = Simulator(250,1e4,val,buy,sell,buy_pt='open',sell_pt='open',exclude_list=exclude_list,daily_limit=10/n_buy) #simulation length in days, starting cash
while True:
    sim.run()

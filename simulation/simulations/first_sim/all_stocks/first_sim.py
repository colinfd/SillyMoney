from simulation import Simulator
import numpy as np
from simulation.funs import running_mean,mean_disp

##############################################
#FUNCTIONS FOR USE IN SIMULATOR
##############################################
def val(stock_name):
    prices = sim.read_stock(stock_name)
    means = running_mean(prices)
    if prices[-1] > means[-1]:
        return mean_disp(prices,means)
    else:
        return 0

def sell(val_dict, held_stocks):
    sell_dict = {}
    for stock_name in held_stocks:
        if held_stocks[stock_name] > 0:
            sell_dict[stock_name] = held_stocks[stock_name]
    return sell_dict

def buy(val_dict,cash,market_prices):
    vals = [(stock_name,val_dict[stock_name]) for stock_name in val_dict]
    vals = sorted(vals,key = lambda x : x[1],reverse=True)
    
    buy_dict = {}
    n = 5
    for i in range(n):
        buy_dict[vals[i][0]] = int(cash/n/market_prices[vals[i][0]])
    return buy_dict


##############################################i
#RUN SIMULATOR
##############################################
sim = Simulator(250,1e4,val,buy,sell)
while True:
    sim.run()

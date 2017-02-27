from simulation import Simulator
from prettytable import PrettyTable
import glob
import sys
import pickle

def val(stock_name):
    """
    Take the name of a stock and return a scalar that is used to evaluate its investment value.
    sim.read_stock(stock_name) returns stock data up to the current day
    """
    prices = sim.read_stock(stock_name,start_i=start_i,end_i=end_i,pt='open')
    diff = [prices[-2] - prices[-3], prices[-1] - prices[-2]]
    if diff[1] < 0 and diff[1] > diff[0]:
        return (diff[1] - diff[0])/prices[-1]
    else:
        return 0

data_path = sys.argv[1]
if len(sys.argv) == 3:
    n_bak = int(sys.argv[2]) #find candidates on most recent day - n_bak
    start_i = -(3 + n_bak)
    end_i = -(1 + n_bak - 1)
else:
    n_bak = 0
    start_i = -3
    end_i = None

n_days = len(pickle.load(open('%s/A.pkl'%data_path))['data'])

sim = Simulator(0,1,val,val,val,dates=[0]*(n_days),data_path=data_path)
pkls = glob.glob('%s/*.pkl'%data_path)
stock_names = [pkl.split('/')[-1][:-4] for pkl in pkls]

sorted_stocks = [None]*len(stock_names)
for i,stock_name in enumerate(stock_names):
    sorted_stocks[i] = [stock_name,val(stock_name)]

sorted_stocks.sort(key=lambda x: x[1],reverse=True)
table = PrettyTable(['Stock','Value','Open','1% Volume Price ($k)'])

for stock_name,value in sorted_stocks[:10]:
    try:
        price = sim.read_stock(stock_name,start_i=start_i,end_i=end_i,pt='open')[-1]
        volume = sim.read_stock(stock_name,start_i=start_i,end_i=end_i,pt='volume')[-1]
        table.add_row([stock_name,value,"%.2f"%price,int(volume/100*price)/1000])
    except:
        print stock_name

print table

from simulation import Simulator
from prettytable import PrettyTable
import glob

def val(stock_name):
    """
    Take the name of a stock and return a scalar that is used to evaluate its investment value.
    sim.read_stock(stock_name) returns stock data up to the current day
    """
    prices = sim.read_stock(stock_name,start_i=0,end_i=3)
    diff = [prices[-2] - prices[-3], prices[-1] - prices[-2]]
    if diff[1] < 0 and diff[1] > diff[0]:
        return (diff[1] - diff[0])/prices[-1]
    else:
        return 0

sim = Simulator(0,1,val,val,val,dates=[0]*3,data_path='data/')
pkls = glob.glob('data/*.pkl')
stock_names = [pkl.split('/')[-1][:-4] for pkl in pkls]

sorted_stocks = [None]*len(stock_names)
for i,stock_name in enumerate(stock_names):
    sorted_stocks[i] = [stock_name,val(stock_name)]

sorted_stocks.sort(key=lambda x: x[1],reverse=True)
table = PrettyTable(['Stock','Value','Open','Volume'])

for stock_name,value in sorted_stocks:
    try:
        table.add_row([stock_name,value,sim.read_stock(stock_name,start_i=0,end_i=3),sim.read_stock(stock_name,pt='volume',start_i=0,end_i=3)])
    except:
        print stock_name

print table

from simulation import Simulator
import matplotlib.pyplot as plt
import numpy as np
import pickle

def dummy():
    return

def diff2(prices):
    diff = [prices[-2] - prices[-3], prices[-1] - prices[-2]]
    if diff[1] < 0 and diff[1] > diff[0]:
        return (diff[1] - diff[0])/prices[-1]
    else:
        return 0

def histogram(data,n,title=None,n_sig=1):
    mean = data.mean(); std = data.std()
    outliers = data[np.abs(data - mean) > n_sig * std]
    data = data[np.abs(data - mean) < n_sig * std]
    new_mean = data.mean()
    new_std = data.std()
    plt.figure()
    plt.hist(data,n)
    plt.title('%s (mean = %.2f/%.2f, std = %.2f/%.2f))'%(title,mean,new_mean,std,new_std))
    
    if len(outliers) > 1:
        plt.axes([0.2,0.65,0.2,0.2]) #inset
        plt.hist(outliers,n)
        plt.gca().tick_params(axis='both',labelsize=4)
        plt.title('Outliers > %d $\sigma$'%n_sig,fontsize=6)

n_days = 1771
sim = Simulator(n_days,0,dummy,dummy,dummy,n_stocks=10)

if True:
    val_fun = diff2
    daily_percs = []
    descriptor = []
    for stock_name in sim.stock_names:
        data = sim.read_stock(stock_name,start_i=0,end_i=n_days-1)
        last = None
        for i in range(len(data)):
            if "%s"%data[i] == 'nan':
                last = None
                continue
            elif last != None and last != 0:
                d = (data[i] - last)/last*100
                if "%s"%d == 'nan' or "%s"%d == 'inf': 
                    last == None
                    continue
                try:
                    descriptor.append(diff2(data[:i]))
                except IndexError:
                    last = data[i]
                    continue
                daily_percs.append(d)
            last = data[i]
    daily_percs = np.array(daily_percs)
    product = daily_percs*np.array(descriptor)
    product = product[product != 0]
    #descriptor = descriptor[descriptor != 0]
    #product = product/np.array(descriptor)
    #pickle.dump(daily_percs,open('daily_percs.pkl','w'))
    #pickle.dump(product,open('diff2_daily_percs.pkl','w'))
else:
    product = pickle.load(open('diff2_daily_percs.pkl'))
    #daily_percs = pickle.load(open('daily_percs.pkl'))

histogram(product[:],50,n_sig=5)
histogram(np.array(daily_percs)[:],50)

plt.figure()
zipped = [[descriptor[i], daily_percs[i]] for i in range(len(descriptor))]
zipped.sort(key=lambda x: x[0],reverse=True)
sorted_dp = [zipped[i][1] for i in range(len(zipped))]
sorted_dp = np.array(sorted_dp)
del_list = []
for i in range(len(sorted_dp)):
    if sorted_dp[i] > 900: del_list.append[i]
sorted_dp = np.delete(sorted_dp,del_list)
for i in range(len(sorted_dp)):
    plt.plot(i,sorted_dp[:i].mean(),'-ko')
exit()
plt.show()

plt.figure()
plt.plot(descriptor,daily_percs,'ro',markersize=4)
plt.show()

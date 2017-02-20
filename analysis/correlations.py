import pickle
import numpy as np
import glob
import matplotlib.pyplot as plt

pt = 0
name = 'OPEN'

def scrape_data():
    stock_pkls = glob.glob('../data/*.pkl')
    #stock_pkls = stock_pkls[:100]

    data = []
    for i,pkl in enumerate(stock_pkls):
        f = open(pkl)
        stock = pickle.load(f)
        f.close()
        
        vals = [day[pt] for day in stock['data']]
        for j,val in enumerate(vals):
            if val == 'N/A':
                vals[j] = np.nan
            else:
                vals[j] = float(val)
        data.append(vals)
        print "%.1f%%"%(i/float(len(stock_pkls))*100)
    return data

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

def rms_disp(prices):
    #return rms_disp of stock from running_mean
    prices = np.array(prices)
    means = np.array(running_mean(prices))
    rms = np.sqrt(np.mean(((prices-means)/means)**2))*100
    return rms

def mean(prices):
    return np.mean(prices)

def norm_var(prices):
    return np.std(running_mean(prices))/mean(prices)

def correlation(fun1,fun2):
    plt.figure()
    try:
        f = open("%s_%s.pkl"%(fun1.__name__,name))
        x_data = pickle.load(f)
        f.close()
    except:
        data = scrape_data()
        x_data = [fun1(i) for i in data]
        f = open("%s_%s.pkl"%(fun1.__name__,name),'w')
        pickle.dump(x_data,f)
        f.close()
    try:
        f = open("%s_%s.pkl"%(fun2.__name__,name))
        y_data = pickle.load(f)
        f.close()
    except:
        try:
            y_data = [fun2(i) for i in data]
        except:
            data = scrape_data()
            y_data = [fun2(i) for i in data]
        f = open("%s_%s.pkl"%(fun2.__name__,name),'w')
        pickle.dump(y_data,f)
        f.close()

    plt.plot(x_data,y_data,'ro')
    plt.xlabel(fun1.__name__)
    plt.ylabel(fun2.__name__)

correlation(mean,rms_disp)
correlation(mean,norm_var)
correlation(rms_disp,norm_var)

plt.show()

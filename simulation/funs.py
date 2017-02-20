import numpy as np

##############################################i
#HELPER FUNCTIONS
##############################################
def running_mean(prices,n=3):
    ret = np.cumsum(prices, dtype=np.float16)
    ret[n:] = ret[n:] - ret[:-n]
    for i in range(n-1): ret = np.insert(ret,0,ret[n-1])
    return ret[n - 1:] / n

def mean_disp(prices,means):
    #return average displacement of prices from means in %
    return np.mean(np.abs(prices-means)/means)*100

def norm_std(prices):
    return np.std(running_mean(prices))/mean(prices)

def running_mean_old(prices,n=5):
    out = np.zeros(len(prices),dtype=np.float16)
    for i,p in enumerate(prices):
        if i < n:
            out[i] = np.mean(prices[:i+n+1])
        elif i > len(prices) - n:
            out[i] = np.mean(prices[i-n:])
        else:
            out[i] = np.mean(prices[i-n:i+n+1])

    return out

import sys
import matplotlib.pyplot as plt
import glob
import numpy as np

def read_log(fname):
    f = open(log)
    lines = f.readlines()
    f.close()
    
    vals = np.zeros(simlength)
    
    i = 0
    for line in lines:
        if line.split(':')[0] == 'Value':
            vals[i] = line.split(':')[1]
            i += 1

    return vals

def get_simlength(fname):
    f = open(log)
    lines = f.readlines()
    f.close()
    return len(lines)/7



dirname = sys.argv[1]
simlength = 250

if dirname[-4:] == '.log':
    logs = [dirname]
else:
    logs = glob.glob(dirname + '/*.log')
del_list = []
for i,log in enumerate(logs):
    if get_simlength(log) != simlength:
        del_list.append(i)

#remove logs with the incorrect # of days
del_list.sort(reverse=True)
for d in del_list:
    del logs[d]

dates = [log.split('/')[-1][:-4] for log in logs]
data = np.zeros((len(logs),simlength))

for i,log in enumerate(logs):
    data[i,:] = read_log(log)
    plt.plot(data[i])
if len(logs) < 6:
    plt.legend(logs,loc=2)
    plt.show()

def histogram(data,n,title=None,n_sig=5):
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



#end total value
histogram(data[:,-1],50,title='Total value after %d days'%simlength,n_sig=1)

#daily % earnings
de = (np.diff(data,axis=1)/data[:,:-1]*100).flatten()
histogram(de,30,title='% Daily Earnings',n_sig=3)

plt.show()

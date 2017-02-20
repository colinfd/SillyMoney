import sys
import matplotlib.pyplot as plt
import glob

dirname = sys.argv[1]
logs = glob.glob(dirname + '/*.log')

for log in logs:
    vals = []
    f = open(log)
    lines = f.readlines()
    f.close()

    for line in lines:
        if line.split(':')[0] == 'Value':
            vals.append(line.split(':')[1])

    plt.plot(vals)

#plt.legend([log.split('/')[-1][:-4] for log in logs])
plt.show()

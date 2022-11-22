import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt("results.csv",delimiter=",")
print(data)
col=-1
vel_plot=[data[0][col]]
for i, row in enumerate(data[1:-1]):
    i+=1
    if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
        vel_plot.append(np.nan)
    else:
        vel_plot.append(row[col])
vel_plot.append(data[-1][col])

window=10
vel_ave=vel_plot[:window]
for i,row in enumerate(vel_plot[window:]):
    i+=window
    ave=np.average(vel_plot[i-window:i])
    vel_ave.append(ave)
plt.plot(data[:,0],vel_plot)
plt.plot(data[:,0],vel_ave)
plt.show()
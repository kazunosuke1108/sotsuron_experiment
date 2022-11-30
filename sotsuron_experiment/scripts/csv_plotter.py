import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt("results.csv",delimiter=",")
print(data)

col=1
x_plot=[data[0][col]]
for i, row in enumerate(data[1:-1]):
    i+=1
    if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
        x_plot.append(np.nan)
    else:
        x_plot.append(row[col])
x_plot.append(data[-1][col])

col=2
y_plot=[data[0][col]]
for i, row in enumerate(data[1:-1]):
    i+=1
    if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
        y_plot.append(np.nan)
    else:
        y_plot.append(row[col])
y_plot.append(data[-1][col])

col=3
z_plot=[data[0][col]]
for i, row in enumerate(data[1:-1]):
    i+=1
    if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
        z_plot.append(np.nan)
    else:
        z_plot.append(row[col])
z_plot.append(data[-1][col])

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
plt.scatter(data[:,0],x_plot,label="x")
plt.scatter(data[:,0],y_plot,label="y")
plt.scatter(data[:,0],z_plot,label="z")
# plt.plot(data[:,0],vel_plot,label="vel_raw")
# plt.plot(data[:,0],vel_ave,label="vel_ave")
plt.legend()
plt.show()
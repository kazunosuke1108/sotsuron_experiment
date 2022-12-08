import os
import json
import numpy as np
import matplotlib.pyplot as plt
# # csv
# csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/results.csv"

# # json
# jsn_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/velocity.json"

# data=np.loadtxt(csv_path,delimiter=",")
# print(data)

# col=1
# x_plot=[data[0][col]]
# for i, row in enumerate(data[1:-1]):
#     i+=1
#     if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
#         x_plot.append(np.nan)
#     else:
#         x_plot.append(row[col])
# x_plot.append(data[-1][col])

# col=2
# y_plot=[data[0][col]]
# for i, row in enumerate(data[1:-1]):
#     i+=1
#     if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
#         y_plot.append(np.nan)
#     else:
#         y_plot.append(row[col])
# y_plot.append(data[-1][col])

# col=3
# z_plot=[data[0][col]]
# for i, row in enumerate(data[1:-1]):
#     i+=1
#     if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
#         z_plot.append(np.nan)
#     else:
#         z_plot.append(row[col])
# z_plot.append(data[-1][col])

csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/results.csv"
data=np.loadtxt(csv_path,delimiter=",")
t=data[:,0]
dpt=data[:,3]

estm_dpt_history=[]
for i in range(len(t)):
    try:
        a,b=np.polyfit(t[:i],dpt[:i],1)
        linear_list=a*t[:i]+b
        estm_dpt=linear_list[-1]
        print("estimated current depth: ",estm_dpt)
        estm_dpt_history.append(estm_dpt)
        if estm_dpt<21:
            print(f"a={a}, b={b}")
            error=dpt-estm_dpt
            print(error)
            break
    except TypeError:
        pass
plt.plot(t,dpt,label="dpt")
plt.plot(t[:len(linear_list)],linear_list,label="estimated dpt")
plt.legend()
plt.show()
print(max(estm_dpt_history))

# 線形近似


# 0.6m/s 全部記録した場合：a=-0.5926943900954349, b=989834174.871474
# 0.6m/s 前半100個のみ記録した場合：a=-0.7386501610544312
# 0.6m/s 前半20個から100個まで記録した場合：a=-0.6296779577545105,

# col=-1
# vel_plot=[data[0][col]]
# for i, row in enumerate(data[1:-1]):
#     i+=1
#     if abs(row[col]-data[i-1][col])>2000 or abs(row[col]-data[i+1][col])>2000:
#         vel_plot.append(np.nan)
#     else:
#         vel_plot.append(row[col])
# vel_plot.append(data[-1][col])

# window=10
# vel_ave=vel_plot[:window]
# for i,row in enumerate(vel_plot[window:]):
#     i+=window
#     ave=np.average(vel_plot[i-window:i])
#     vel_ave.append(ave)



# plt.plot(data[:,0],x_plot,label="x")
# # plt.plot(data[:,0],y_plot,label="y")
# plt.plot(data[:,0],z_plot,label="z")
# # plt.plot(data[:,0],vel_plot,label="vel_raw")
# plt.plot(t_list,linear_list,label="z_linear")

# plt.legend()
# # plt.show()
# plt.savefig(os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/results.png")
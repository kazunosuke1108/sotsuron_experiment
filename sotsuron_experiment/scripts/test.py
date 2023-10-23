import os
import matplotlib.pyplot as plt
import pandas as pd


csvpath="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231014/csv/_2023-10-14-19-43-12.bag_tf.csv"
data=pd.read_csv(csvpath,names=["t","x","y","z"])



plt.plot(data["t"],data["x"],label="x")
plt.plot(data["t"],data["y"],label="y")
plt.plot(data["t"],data["z"],label="z")
plt.legend()
plt.grid()
plt.savefig(csvpath[:-4]+".png")
plt.show()

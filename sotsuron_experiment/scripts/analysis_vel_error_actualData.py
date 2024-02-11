import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams["font.size"] = 24

odom_to_zed_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_odom_to_zed.csv"
zed_to_hmn_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_zed_to_hmn.csv"
odom_to_hmn_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_odom_to_hmn.csv"

zR=pd.read_csv(odom_to_zed_csv_path,names=["t","x","y","z"])
zHR=pd.read_csv(zed_to_hmn_csv_path,names=["t","x","y","z"])
zH=pd.read_csv(odom_to_hmn_csv_path,names=["t","x","y","z"])
start_time=zH["t"].iat[0]+0
end_time=zH["t"].iat[0]+15
zR=zR[zR["t"]>start_time]
zHR=zHR[zHR["t"]>start_time]
zH=zH[zH["t"]>start_time]
zR=zR[zR["t"]<end_time]
zHR=zHR[zHR["t"]<end_time]
zH=zH[zH["t"]<end_time]
plt.plot(zHR["t"],np.sqrt(zHR["y"]**2+zHR["z"]**2),"o-",label="distance H&R")
plt.plot(zR["t"],zR["x"],"o-",label="xR")
plt.plot(zH["t"],zH["x"],"o-",label="xH")
plt.xlabel("Time $\it{t}$ [s]")
plt.ylabel("Position $\it{x}$ [m]")
plt.legend()
plt.savefig("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_odom_to_zed_to_hmn.png",dpi=500)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

odom_to_zed_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_odom_to_zed.csv"
zed_to_hmn_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_zed_to_hmn.csv"
odom_to_hmn_csv_path="C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/velocity_error/_2023-12-21-10-22-39_odom_to_hmn.csv"

zR=pd.read_csv(odom_to_zed_csv_path,names=["t","x","y","z"])
zHR=pd.read_csv(zed_to_hmn_csv_path,names=["t","x","y","z"])
zH=pd.read_csv(odom_to_hmn_csv_path,names=["t","x","y","z"])
plt.plot(zHR["t"],np.sqrt(zHR["y"]**2+zHR["z"]**2),"o-")
plt.plot(zR["t"],zR["x"],"o-")
plt.plot(zH["t"],zH["x"],"o-")
plt.show()
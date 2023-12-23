import numpy as np
import pandas as pd

data=pd.read_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/hayashide_robot_03_all.csv",header=None)
data=data.iloc[:3]

for column in data.columns:
    data[column].iat[2]=str(data[column].iat[0])+"_"+str(data[column].iat[1])
print(data)

data_out=data.iloc[2]
print(data_out)
data_out.to_csv("C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231220_VICON/prefix.csv")
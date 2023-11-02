import matplotlib.pyplot as plt
import pandas as pd

data=pd.read_csv("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/dev_lrf/predictions_history.csv",names=["t","x","y"])
plt.plot(data["t"],data["x"])
plt.show()
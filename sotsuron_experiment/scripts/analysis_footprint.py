from glob import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style as mplstyle
from matplotlib import patches
import pandas as pd
from pprint import pprint
import pickle

from analysis_management import *
from analysis_initial_processor import *
path_management,csv_labels,color_dict=management_initial()
plt.rcParams["figure.figsize"] = (10,15)
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.family'] = 'Times New Roman'
rows = 3
cols = 1
fig, axes = plt.subplots(nrows=rows, ncols=cols)

denoise_dir_path=path_management["denoise_3d_csv_path"]
denoise_paths=sorted(glob(denoise_dir_path+"/*"))
pprint(denoise_paths)
for denoise_path in denoise_paths:
    if "12_00_00" not in denoise_path:
        continue
    data=pd.read_csv(denoise_path,header=0)
    print(data)

    frames = []

    for i in range(len(data)):
        l_footprint_xy=axes[0].scatter(data["l_foot_x"].iloc[i],data["l_foot_y"].iloc[i],color="r",s=3)
        r_footprint_xy=axes[0].scatter(data["r_foot_x"].iloc[i],data["r_foot_y"].iloc[i],color="b",s=3)
        l_footprint_history_xy=axes[0].scatter(data["l_foot_x"].iloc[:i],data["l_foot_y"].iloc[:i],color="r",s=1)
        r_footprint_history_xy=axes[0].scatter(data["r_foot_x"].iloc[:i],data["r_foot_y"].iloc[:i],color="b",s=1)
        axes[0].set_xlabel("Hallway Direction [m]")
        axes[0].set_ylabel("Width Direction [m]")
        axes[0].set_xlim([-1,6])
        axes[0].set_ylim([-2,2])
        axes[0].set_title(f"path (index={i})")
        axes[0].set_aspect('equal')

        l_footprint_tx=axes[1].scatter(data["timestamp"].iloc[i],data["l_foot_x"].iloc[i],color="r",s=3)
        r_footprint_tx=axes[1].scatter(data["timestamp"].iloc[i],data["r_foot_x"].iloc[i],color="b",s=3)
        l_footprint_history_tx=axes[1].scatter(data["timestamp"].iloc[:i],data["l_foot_x"].iloc[:i],color="r",s=1)
        r_footprint_history_tx=axes[1].scatter(data["timestamp"].iloc[:i],data["r_foot_x"].iloc[:i],color="b",s=1)
        axes[1].set_xlabel("Time [s]")
        axes[1].set_ylabel("Hallway Direction [m]")
        axes[1].set_xlim([data["timestamp"].min(),data["timestamp"].max()])
        axes[1].set_ylim([-1,6])
        axes[1].set_title(f"path (index={i})")

        l_footprint_ty=axes[2].scatter(data["timestamp"].iloc[i],data["l_foot_y"].iloc[i],color="r",s=3)
        r_footprint_ty=axes[2].scatter(data["timestamp"].iloc[i],data["r_foot_y"].iloc[i],color="b",s=3)
        l_footprint_history_ty=axes[2].scatter(data["timestamp"].iloc[:i],data["l_foot_y"].iloc[:i],color="r",s=1)
        r_footprint_history_ty=axes[2].scatter(data["timestamp"].iloc[:i],data["r_foot_y"].iloc[:i],color="b",s=1)
        axes[2].set_xlabel("Time [s]")
        axes[2].set_ylabel("Width Direction [m]")
        axes[2].set_xlim([data["timestamp"].min(),data["timestamp"].max()])
        axes[2].set_ylim([-1.3,1.3])
        axes[2].set_title(f"path (index={i})")

        # l_footprint_ty=axes[1,0].scatter(data["timestamp"].iloc[i],data["l_foot_y"].iloc[i],color="r",s=3)
        # r_footprint_ty=axes[1,0].scatter(data["timestamp"].iloc[i],data["r_foot_y"].iloc[i],color="b",s=3)
        # l_footprint_history_ty=axes[1,0].scatter(data["timestamp"].iloc[:i],data["l_foot_y"].iloc[:i],color="r",s=1)
        # r_footprint_history_ty=axes[1,0].scatter(data["timestamp"].iloc[:i],data["r_foot_y"].iloc[:i],color="b",s=1)
        # axes[1,0].set_xlabel("Time [s]")
        # axes[1,0].set_ylabel("Width Direction [m]")
        # axes[1,0].set_xlim([data["timestamp"].min(),data["timestamp"].max()])
        # axes[1,0].set_ylim([-2,2])
        # axes[1,0].set_title(f"path (index={i})")
        frames.append([l_footprint_xy, r_footprint_xy,l_footprint_history_xy, r_footprint_history_xy,l_footprint_tx, r_footprint_tx,l_footprint_history_tx, r_footprint_history_tx,l_footprint_ty, r_footprint_ty,l_footprint_history_ty, r_footprint_history_ty])
        print(i,len(data))
        # try:
        #     pausetime=data['timestamp'].iloc[i+1]-data['timestamp'].iloc[i]
        #     print(f"pause for {pausetime} s")
        #     if pausetime>0:
        #         plt.pause(pausetime)
        #     else:
        #         plt.pause(0.1)
        # except IndexError:
        #     plt.pause(0.1)
        # plt.cla()
        # plt.pause(0.01)
    # plt.cla()
    ani = animation.ArtistAnimation(fig, frames, interval=5)
    ani.save(f"C:/Users/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/analysis/mp4/{os.path.basename(denoise_path[:-4])}_foot.mp4", writer='ffmpeg')


#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from glob import glob

bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_zed/ytlab_zed_modules/rosbag/*"))
print(bags)

for bag in bags:#[12:]:
    print(bag)
    bag_basename=os.path.basename(bag)
    csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0207/csv/"+bag_basename[:-4]+".csv"
    play_cmd=f"roslaunch sotsuron_experiment velocity_plotter.launch bag_basename:={bag_basename[:-4]}"
    # runcmd=sp.call(cmd.split())
    # print(runcmd)
    os.system(play_cmd)



"""
rosbag play
path_subscriberでcsvに書き出す
path_plotterで保存
"""
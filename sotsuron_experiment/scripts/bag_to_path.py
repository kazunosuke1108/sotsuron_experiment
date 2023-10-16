#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess as sp
from glob import glob

# bags=sorted(glob("/media/hayashide/KIOXIA/hayashide/rosbag/0203/*"))
# bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_hsr/ytlab_hsr_modules/rosbag/EtoE/*"))
# bags=sorted(glob("/media/hayashide/KIOXIA/hayashide/rosbag/0203/*"))
bags=["/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/20231014/_2023-10-14-19-43-12.bag"]
# bags=["/media/hayashide/KIOXIA/hayashide/rosbag/0203/20230203_d_060_3_Yoshinari.bag",
#       "/media/hayashide/KIOXIA/hayashide/rosbag/0220/20230220_d_090_30_shingo.bag"]
print(bags)

# partial_bags=[]
# for bag in bags:
#     if "_23_" in bag or "_24_" in bag or "_26_" in bag:
#         partial_bags.append(bag)

for bag in bags:# partial_bags:
# for bag in bags:
    print(bag)
    bag_basename=os.path.basename(bag)
    csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20231014/csv/"+bag_basename[:-4]+".csv"
    odom_csv_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20231014/odom_csv/"+bag_basename[:-4]+".csv"
    avi_dir_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20231014/movie/"
    avi_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20231014/movie/"+bag_basename[:-4]+".avi"
    skeleton_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/20231014/skeleton_movie/"+bag_basename[:-4]+".mp4"
    play_cmd=f"roslaunch sotsuron_experiment path_plotter.launch avi_basename:={bag_basename[:-4]} bag_basename:={bag_basename[:-4]} bag_path:={bag} csv_path:={csv_path} odom_csv_path:={odom_csv_path} save_path:={avi_path}"
    # runcmd=sp.call(cmd.split())
    # print(runcmd)
    os.system(play_cmd)
    
    # graph_cmd="python3 path_plotter_14_7F.py"
    # os.system(graph_cmd)

    # mp4_cmd=f"python3 conv_avi_turn_mp4.py {avi_dir_path}"
    # os.system(mp4_cmd)

    # skeleton_cmd=f"python3 skeleton_movie.py {avi_path} {skeleton_path}"
    # os.system(skeleton_cmd)

    # os.system("git add .")
    # os.system("git commit -m 'auto push for skeleton'")
    # os.system("git push origin master")

"""
rosbag play
path_subscriberでcsvに書き出す
path_plotterで保存
"""
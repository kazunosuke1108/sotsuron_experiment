from glob import glob
from pprint import pprint
import os
import subprocess
# from git_auto_push import git_auto_push

# この手前まで
# /home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231020/csv/09_07_00__2023-10-21-17-10-43_tf.csv
# bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_07_*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_08_*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_09_*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_10_*"))
# bags+=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/10*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/11*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/12*"))
# pprint(bags)
# bags=["/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/20231020/03_00_00__2023-10-20-17-09-06.bag"]
# bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/13*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/14*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/15*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/16*"))
bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/0*_00_0*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/0*_01_0*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/0*_03_0*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/0*_06_0*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/0*_08_0*"))
bags=sorted(bags)
pprint(bags)
for bag in bags:
    launch_command = f"roslaunch sotsuron_experiment ras_postprocessor_2.launch bag_name:={os.path.basename(bag)[:-4]}"
    subprocess.run(launch_command, shell=True, check=True)
# print("ok")
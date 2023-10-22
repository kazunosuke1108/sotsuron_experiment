from glob import glob
from pprint import pprint
import os
import subprocess
from git_auto_push import git_auto_push

# この手前まで
# /home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/results/20231020/csv/09_07_00__2023-10-21-17-10-43_tf.csv
bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_07_*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_08_*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_09_*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/09_10_*"))
bags+=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/10*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/11*"))+sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/12*"))
# pprint(bags)
for bag in bags:
    launch_command = f"roslaunch sotsuron_experiment ras_postprocessor.launch bag_name:={os.path.basename(bag)[:-4]}"
    subprocess.run(launch_command, shell=True, check=True)
# print("ok")
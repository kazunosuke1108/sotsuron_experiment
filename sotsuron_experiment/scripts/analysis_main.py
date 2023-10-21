from glob import glob
from pprint import pprint
import os
import subprocess
from git_auto_push import git_auto_push

bags=sorted(glob("/home/hayashide/catkin_ws/src/ytlab_rosbag/rosbag/03*"))
pprint(bags)
for bag in bags:
    launch_command = f"roslaunch sotsuron_experiment ras_postprocessor.launch bag_name:={os.path.basename(bag)[:-4]}"
    subprocess.run(launch_command, shell=True, check=True)
# print("ok")
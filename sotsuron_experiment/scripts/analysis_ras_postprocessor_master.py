import os
from glob import glob

rosbag_dir="/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag"
resultsdir="/home/hayashide/catkin_ws/src/sotsuron_experiment/results"
daydir=sorted(glob(rosbag_dir+"/*"))
daydir=daydir[-2]

rosbagpaths=sorted(glob(daydir+"/02_otayu/*"))
for rosbagpath in rosbagpaths:
    bag_name=os.path.basename(rosbagpath)[:-4]
    bag_path=rosbagpath
    result_path=resultsdir+f"/{bag_name}"
    os.makedirs(result_path,exist_ok=True)

    os.system(f"roslaunch sotsuron_experiment ras_postprocessor_3.launch bag_name:={bag_name} bag_path:={bag_path} result_path:={result_path}")



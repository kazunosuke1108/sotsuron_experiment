import os
from glob import glob

rosbag_dir="/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag"
resultsdir="/home/hayashide/catkin_ws/src/sotsuron_experiment/results"
daydir=sorted(glob(rosbag_dir+"/*"))
daydir=daydir[-2]
print(daydir)
rosbagpaths=sorted(glob(daydir+"/06_murayama/success/*"))
rosbagpaths+=sorted(glob(daydir+"/07_yoshinari/success/*"))
rosbagpaths+=sorted(glob(daydir+"/08_motoyama/success/*"))
rosbagpaths+=sorted(glob(daydir+"/09_konishi/success/*"))
# rosbagpaths+=sorted(glob(daydir+"/05_inoue/success/*"))
# rosbagpaths=[
#     "/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/20231219/01_takahashi/success/_2023-12-19-13-54-12.bag",
#     "/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/20231219/05_inoue/success/_2023-12-19-20-30-09.bag",
# ]
# rosbagpaths=sorted(glob(daydir+"/*"))
print(rosbagpaths)
for rosbagpath in rosbagpaths:
    bag_name=os.path.basename(rosbagpath)[:-4]
    bag_path=rosbagpath
    result_path=resultsdir+f"/{bag_name}"
    os.makedirs(result_path,exist_ok=True)

    os.system(f"roslaunch sotsuron_experiment ras_postprocessor_3.launch bag_name:={bag_name} bag_path:={bag_path} result_path:={result_path}")



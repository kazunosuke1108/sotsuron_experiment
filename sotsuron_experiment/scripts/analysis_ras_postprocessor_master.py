import os
from glob import glob
from pprint import pprint

rosbag_dir="/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag"
resultsdir="/home/hayashide/catkin_ws/src/sotsuron_experiment/results"
daydir=sorted(glob(rosbag_dir+"/*"))
daydir1=daydir[-4]
daydir2=daydir[-2]
print(daydir)
rosbagpaths=sorted(glob(daydir1+"/01_takahashi/success/*"))
rosbagpaths+=sorted(glob(daydir1+"/02_otayu/success/*"))
rosbagpaths+=sorted(glob(daydir1+"/03_koyama/success/*"))
rosbagpaths+=sorted(glob(daydir1+"/04_ohnishi/success/*"))
rosbagpaths+=sorted(glob(daydir1+"/05_inoue/success/*"))
rosbagpaths+=sorted(glob(daydir2+"/06_murayama/success/*"))
rosbagpaths+=sorted(glob(daydir2+"/07_yoshinari/success/*"))
rosbagpaths+=sorted(glob(daydir2+"/08_motoyama/success/*"))
rosbagpaths+=sorted(glob(daydir2+"/09_konishi/success/*"))
# rosbagpaths+=sorted(glob(daydir+"/05_inoue/success/*"))
# rosbagpaths=[
#     "/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/20231219/01_takahashi/success/_2023-12-19-13-54-12.bag",
#     "/home/hayashide/catkin_ws/media/hayashide/KIOXIA/hayashide/rosbag/20231219/05_inoue/success/_2023-12-19-20-30-09.bag",
# ]
# rosbagpaths=sorted(glob(daydir+"/*"))
pprint(rosbagpaths)
# raise TimeoutError
for rosbagpath in rosbagpaths:
    bag_name=os.path.basename(rosbagpath)[:-4]
    bag_path=rosbagpath
    result_path=resultsdir+f"/{bag_name}"
    os.makedirs(result_path,exist_ok=True)

    os.system(f"roslaunch sotsuron_experiment ras_postprocessor_3.launch bag_name:={bag_name} bag_path:={bag_path} result_path:={result_path}")


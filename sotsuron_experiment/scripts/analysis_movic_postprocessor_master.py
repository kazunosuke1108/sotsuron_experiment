import os
from glob import glob
from pprint import pprint

rosbag_dir="/home/hayashide/catkin_ws/media/hayashide/Extreme Pro/hayashide/rosbag/20240204"
resultsdir="/home/hayashide/catkin_ws/src/sotsuron_experiment/results"
hsrbdir=sorted(glob(rosbag_dir+"/h*"))[0]
zeddir=sorted(glob(rosbag_dir+"/z*"))[0]
stereodir=sorted(glob(rosbag_dir+"/s*"))[0]

hsrb_rosbag_paths=sorted(glob(hsrbdir+"/_2024*"))
zed_rosbag_paths=sorted(glob(zeddir+"/*"))
stereo_rosbag_paths=sorted(glob(stereodir+"/*"))

# hsrb_rosbag_paths.reverse()
# zed_rosbag_paths.reverse()
# stereo_rosbag_paths.reverse()

for idx, [hsrb_rosbag_path,zed_rosbag_path,stereo_rosbag_path] in enumerate(zip(hsrb_rosbag_paths,zed_rosbag_paths,stereo_rosbag_paths)):


    trial_id=str(len(hsrb_rosbag_paths)-idx).zfill(2)
    result_dir_path=resultsdir+"/"+os.path.basename(rosbag_dir)+"_"+trial_id
    os.makedirs(result_dir_path,exist_ok=True)
    for rosbag_path in [hsrb_rosbag_path,zed_rosbag_path,stereo_rosbag_path]:
        category=os.path.basename(os.path.split(rosbag_path)[0])
        result_subdir_path=result_dir_path+"/"+category
        os.makedirs(result_subdir_path,exist_ok=True)
        # print(result_subdir_path)
        bag_name=os.path.basename(rosbag_path)[:-4]
        bag_path=rosbag_path
        results_dir_path=result_subdir_path
        # if category=="hsrb":
        #     print(bag_name)
        #     print(bag_path)
        #     print(results_dir_path)
        #     os.system(f"roslaunch sotsuron_experiment movic_postprocessor_hsrb.launch bag_name:={bag_name} results_dir_path:={results_dir_path}")
        if category=="zed":
            print(bag_name)
            print(bag_path)
            print(results_dir_path)
            bigdata_rgb_dir_path=f"/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error/big_data/20240204/{bag_name}"
            os.makedirs(bigdata_rgb_dir_path,exist_ok=True)
            os.system(f"roslaunch sotsuron_experiment movic_postprocessor_zed.launch bag_name:={bag_name} results_dir_path:={results_dir_path} bigdata_rgb_dir_path:={bigdata_rgb_dir_path}")
            

import os
import numpy as np
from glob import glob
import matlab.engine
eng = matlab.engine.start_matlab()

mat_dir_path="/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/07_exp/mat"
csv_dir_path="/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/07_exp/csv"

mat_files=sorted(glob(mat_dir_path+"/*"))
for mat_file in mat_files:
    file_basename=os.path.basename(mat_file)
    content = eng.load(mat_file, nargout=1)
    z8=np.array(content['z8'])
    t=np.array(content['t'])
    np.savetxt(csv_dir_path+"/"+file_basename[:-4]+"_z8.csv",z8,delimiter=",")
    np.savetxt(csv_dir_path+"/"+file_basename[:-4]+"_t.csv",t,delimiter=",")


# content = eng.load("/home/hayashide/kazu_ws/sotsuron_simulator/matlab_ws/1219/results/1219_LRF_daikei_objF/221219_104345_180deg/221219_104345_test.mat", nargout=1)
# # print(np.array(content['z']).shape)
# z=np.array(content['z'])
# t=np.array(content['t'])
# np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/z1219.csv",z,delimiter=",")
# np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/z1219.csv",z,delimiter=",")
# np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/t1219.csv",t,delimiter=",")
# np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/t1219.csv",t,delimiter=",")
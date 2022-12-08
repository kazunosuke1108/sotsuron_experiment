import numpy as np
import matlab.engine
eng = matlab.engine.start_matlab()
content = eng.load("/home/hayashide/kazu_ws/sotsuron_simulator/matlab_ws/1201/results/1208_07hallv3/221208_191150_2Hz/221208_191150_test.mat", nargout=1)
# print(np.array(content['z']).shape)
z=np.array(content['z'])
t=np.array(content['t'])
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/z2hzH.csv",z,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/z2hzH.csv",z,delimiter=",")
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/t2hzH.csv",t,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/t2hzH.csv",t,delimiter=",")
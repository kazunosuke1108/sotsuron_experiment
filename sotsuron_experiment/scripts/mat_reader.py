import numpy as np
import matlab.engine
eng = matlab.engine.start_matlab()
content = eng.load("/home/hayashide/kazu_ws/sotsuron_simulator/matlab_ws/1201/results/1208_07304v2/221208_185015_1.5m20m2Hz/221208_185015_test.mat", nargout=1)
# print(np.array(content['z']).shape)
z=np.array(content['z'])
t=np.array(content['t'])
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/z20.csv",z,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/z20.csv",z,delimiter=",")
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/t20.csv",t,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/t20.csv",t,delimiter=",")
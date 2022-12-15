import numpy as np
import matlab.engine
eng = matlab.engine.start_matlab()
content = eng.load("/home/hayashide/kazu_ws/sotsuron_simulator/matlab_ws/1214/results/1214_dummyData/221214_144524_/221214_144524_test.mat", nargout=1)
# print(np.array(content['z']).shape)
z=np.array(content['z'])
t=np.array(content['t'])
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/z.csv",z,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/z.csv",z,delimiter=",")
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/t.csv",t,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/t.csv",t,delimiter=",")
import numpy as np
import matlab.engine
eng = matlab.engine.start_matlab()
content = eng.load("/home/hayashide/kazu_ws/sotsuron_simulator/matlab_ws/1210/results/1210_parastd4Hz/221210_140704_xmax10_ymin-2/221210_140704_test.mat", nargout=1)
# print(np.array(content['z']).shape)
z=np.array(content['z'])
t=np.array(content['t'])
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/z_x10y-2_kinou.csv",z,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/z_x10y-2_kinou.csv",z,delimiter=",")
np.savetxt("/home/hayashide/kazu_ws/sotsuron_experiment/sotsuron_experiment/scripts/monitor/t_x10y-2_kinou.csv",t,delimiter=",")
np.savetxt("/home/hayashide/ytlab_ros_ws/ytlab_hsr/ytlab_hsr_modules/datas/t_x10y-2_kinou.csv",t,delimiter=",")
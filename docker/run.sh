#!/bin/bash

cd `dirname $0`

# xhost +
xhost +local:user
# xhost + 192.168.1.54
# nvidia-dockerの確認
nvidia-docker &> /dev/null
nvidia_docker_installed=$?

# nvidia-container-toolkitの確認
nvidia-container-toolkit &> /dev/null
nvidia_container_toolkit_installed=$?

# 両方がインストールされていない場合のチェック
if [ $nvidia_docker_installed -ne 0 ] && [ $nvidia_container_toolkit_installed -ne 2 ]; then
    echo $TAG
    echo "=========================================================="
    echo "= nvidia-docker & nvidia-container-toolkit not installed ="
    echo "=========================================================="
else
    echo "=========================" 
    echo "=nvidia docker installed="
    echo "========================="
    # other pc
    
    # ./global_ros_setting.sh
    
    docker run -it \
    --privileged \
    --runtime=nvidia \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -e NVIDIA_DRIVER_CAPABILITIES=all \
    --env=DISPLAY=$DISPLAY \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -v "/home/${USER}/.Xauthority:/home/${USER}/.Xauthority" \
    --env="QT_X11_NO_MITSHM=1" \
    --rm \
    -v "/${PWD}/global_ros_setting.sh:/ros_setting.sh" \
    -v "/${PWD}/ros_workspace:/home/${USER}/catkin_ws/" \
    -v "${PWD}/config/terminator_config:/home/${USER}/.config/terminator/config" \
    -v "/${PWD}/../../sotsuron_simulator:/home/${USER}/catkin_ws/src/sotsuron_simulator" \
    -v "/${PWD}/../sotsuron_experiment:/home/${USER}/catkin_ws/src/sotsuron_experiment" \
    -v "/${PWD}/../third_party:/home/${USER}/catkin_ws/src/third_party" \
    -v "/usr/local/MATLAB:/home/${USER}/catkin_ws/src/MATLAB" \
    -v "${HOME}/MATLAB_installer:/home/${USER}/catkin_ws/src/MATLAB_installer" \
    -v /etc/group:/etc/group:ro \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v /media:/media \
    -v "/${PWD}/../../../ytlab_ros_ws/ytlab_rosbag:/home/${USER}/catkin_ws/src/ytlab_rosbag" \
    -v "/${PWD}/../../../ytlab_ros_ws/ytlab_hsr:/home/${USER}/catkin_ws/src/ytlab_hsr" \
    -v "/$(pwd)/../../../ytlab_ros_ws/ytlab_navigation:/home/${USER}/catkin_ws/src/ytlab_navigation" \
    -v "/$(pwd)/../../../ytlab_ros_ws/ytlab_environment/ytlab_environment_msgs:/home/${USER}/catkin_ws/src/ytlab_environment/ytlab_environment_msgs" \
    -v "/$(pwd)/../../../ytlab_ros_ws/ytlab_environment/ytlab_environment_configs:/home/${USER}/catkin_ws/src/ytlab_environment/ytlab_environment_configs" \
    -v /dev:/dev \
    --net host \
    ${USER}/sotsuron_experiment
fi
    # -v "/${PWD}/../../../ytlab_ros_ws/ytlab_zed:/home/${USER}/catkin_ws/src/ytlab_zed" \
    # git clone https://github.com/facebookresearch/detectron2.git
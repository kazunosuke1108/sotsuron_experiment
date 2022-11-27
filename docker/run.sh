#!/bin/bash

cd `dirname $0`

# xhost +
xhost +local:user
# xhost + 192.168.1.54
nvidia-docker &> /dev/null
if [ $? -ne 0 ]; then
    echo $TAG
    echo "=============================" 
    echo "=nvidia docker not installed="
    echo "============================="
else
    echo "=========================" 
    echo "=nvidia docker installed="
    echo "========================="
    
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
    -v "/$(pwd)/global_ros_setting.sh:/ros_setting.sh" \
    -v "/$(pwd)/ros_workspace:/home/${USER}/catkin_ws/" \
    -v "${PWD}/config/terminator_config:/home/${USER}/.config/terminator/config" \
    -v "/$(pwd)/../../sotsuron_simulator:/home/${USER}/catkin_ws/src/sotsuron_simulator" \
    -v "/$(pwd)/../sotsuron_experiment:/home/${USER}/catkin_ws/src/sotsuron_experiment" \
    -v "/usr/local/MATLAB:/home/${USER}/catkin_ws/src/MATLAB" \
    -v "/home/ytpc2022h/MATLAB_installer:/home/${USER}/catkin_ws/src/MATLAB_installer" \
    -v /etc/group:/etc/group:ro \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v /media:/media \
    -v /dev:/dev \
    --net host \
    ${USER}/whill
fi
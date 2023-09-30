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

    docker build  --tag ${USER}/sotsuron_experiment --build-arg USER=${USER} --build-arg USER_ID=`id -u` --build-arg workspace="/home/${USER}/catkin_ws" .
fi

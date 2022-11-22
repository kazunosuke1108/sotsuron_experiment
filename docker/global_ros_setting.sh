#!/bin/bash

## source 
source ~/catkin_ws/devel/setup.bash
## get ipv4 address
ipv4addr=$(/sbin/ifconfig -a                                 |
            grep inet[^6]                                     |
            sed 's/.*inet[^6][^0-9]*\([0-9.]*\)[^0-9]*.*/\1/' |
            grep '^192\.168\.1\.'                                )
if [ "$TARGET_IP" = "" ] ; then
    ipv4addr="localhost"
fi
## get joy path
# joy_name=Logicool
# get_joy_name=$(ls /dev/input/by-id |
#             grep $joy_name     |
#             grep -v event)
# get_joy_path=/dev/input/by-id/$get_joy_name

CATKIN_HOME=~/catkin_ws
# export TTY_WHILL=/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AB0P5EEG-if00-port0
# export TTY_IMU=/dev/serial/by-id/usb-RT_CORPORATION_RT-USB-9AXIS-00_9AXIS-00-if00
# export JOY_PATH=$get_joy_path
# echo "TTY_WHILL : "$TTY_WHILL
# echo "TTY_IMU : "$TTY_IMU
# echo "JOY_PATH : "$JOY_PATH
## export
# export ros_master=global
export ros_master=local
#export ros_master_global=192.168.1.55
export hsr_ip=192.168.1.47
export whill_ip=192.168.1.144
export dlbox_ip=192.168.1.54

export ROS_HOME=~/.ros

echo "HOSTNAME : "$HOSTNAME
TARGET_IP=$ipv4addr
if [ -z "$TARGET_IP" ] ; then
    echo "ROS_IP is not set."
else
    export ROS_IP=$TARGET_IP
fi
if [ "$ipv4addr" = "" ] ; then
    ipv4addr="localhost"
fi
TARGET_IP=$ipv4addr
if [ ${ros_master} = local ] ; then
    echo "ROS_MASER : LOCAL" 
    export ROS_MASTER_URI=http://$TARGET_IP:11311
else
    echo "ROS_MASER : GLOBAL" 
    export ROS_MASTER_URI=http://$ros_master_global:11311
fi

## alias
cdls()
{
    \cd "$@" && ls
}
alias cd="cdls"
alias cm="cd ${CATKIN_HOME} && catkin_make -DCMAKE_BUILD_TYPE=Release&& cd -"
alias cmpy="cd ${CATKIN_HOME} && catkin_make && source ~/catkin_ws/devel/setup.bash && wstool init && wstool set -y src/geometry2 --git https://github.com/ros/geometry2 -v 0.6.5 && wstool up && rosdep update && rosdep install --from-paths src --ignore-src -y -r && catkin_make --cmake-args -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so && cd -"
# https://answers.ros.org/question/326226/importerror-dynamic-module-does-not-define-module-export-function-pyinit__tf2/
alias cc="cd ${CATKIN_HOME} && rm -rf devel && rm -rf build && cd -"
alias hsrb_mode='export ROS_MASTER_URI=http://${hsr_ip}:11311 export PS1="\[\033[41;1;37m\]<DOCKER HSR_MODE>\[\033[0m\]\w$ "&& echo "ROS_MASTER_URI:"$ROS_MASTER_URI && rosnode kill pose_integrator'
alias whill_mode='export ROS_MASTER_URI=http://${whill_ip}:11311 export PS1="\[\033[41;1;37m\]<DOCKER WHILL_MODE>\[\033[0m\]\w$ "&& echo "ROS_MASTER_URI:"$ROS_MASTER_URI'
alias dlbox_mode='export ROS_MASTER_URI=http://${dlbox_ip}:11311 export PS1="\[\033[41;1;37m\]<DOCKER DLBOX_MODE>\[\033[0m\]\w$ "&& echo "ROS_MASTER_URI:"$ROS_MASTER_URI'

# chmod a+x ~/catkin_ws/src/ytlab_navigation/ytlab_navigation_msgs/cfg/DWACostParams.cfg
# sudo mkdir -p ~/.config/Ultralytics
sudo mkdir -p ~/.config/matplotlib
sudo chmod -R 777 /home/hayashide/.config/matplotlib
sudo chmod -R 777 /media

## echo
echo "ROS_IP:"$ROS_IP
echo "ROS_MASTER_URI:"$ROS_MASTER_URI
echo "==========================="
echo "=LOADED GLOBAL ROS SETTING="
echo "==========================="


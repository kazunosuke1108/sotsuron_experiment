 #!/bin/bash -x

cd `dirname $0`

nvidia-docker &> /dev/null
if [ $? -ne 0 ]; then
    echo "=============================" 
    echo "=nvidia docker not installed="
    echo "============================="
else
    echo "=========================" 
    echo "=nvidia docker installed="
    echo "========================="
    docker build  --tag ${USER}/whill --build-arg USER=${USER} --build-arg USER_ID=`id -u` --build-arg workspace="/home/${USER}/catkin_ws" .
fi

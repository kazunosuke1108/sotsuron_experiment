# ytlab_zed

## Usage
1. Clone
```
$ git clone --recursive git@github.com:Takahashi-Lab-Keio/ytlab_zed.git
$ cd ytlab_zed
$ git submodule update --init --recursive
```

2. Docker build
```
$ cd ytlab_zed/docker
$ ./build
$ ./run
$ cm
exit from container
```

3. RUN ROS launch file
```
$ cd ytlab_zed/docker
$ ./run
$ roslaunch ytlab_zed_modules user_zed.launch
```

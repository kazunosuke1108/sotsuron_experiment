#! /usr/bin/python3
# -*- coding: utf-8 -*- 

import rospy 
from nav_msgs.msg import Odometry   
import tf
import sys
from tf.transformations import euler_from_quaternion
import numpy as np

_odom_x, _odom_y, _odom_theta = 0.0, 0.0, 0.0

odom_csv_path=sys.argv[1]

# csv_path=f"/home/hayashide/catkin_ws/src/sotsuron_experiment/scripts/monitor/{bag_basename}.csv"
odom_history=[]
zero_path="/home/hayashide/catkin_ws/src/sotsuron_experiment/scripts/sources/odom_zero.csv"

zero_data=np.loadtxt(zero_path,delimiter=",")
np.average(zero_data[:,0]),np.average(zero_data[:,1]),np.average(zero_data[:,2])

def callback_odom(msg):
    global _odom_x, _odom_y, _odon_theta 
    _odom_x = msg.pose.pose.position.x  
    _odom_y = msg.pose.pose.position.y  
    qx = msg.pose.pose.orientation.x
    qy = msg.pose.pose.orientation.y
    qz = msg.pose.pose.orientation.z
    qw = msg.pose.pose.orientation.w
    q = (qx, qy, qz, qw)
    e = euler_from_quaternion(q)
    _odom_theta = e[2] 

    # _odom_x-=np.average(zero_data[:,0])
    # _odom_y-=np.average(zero_data[:,1])
    # _odom_theta-=np.average(zero_data[:,2])
    rospy.loginfo("Odomery: x=%s y=%s theta=%s", _odom_x, _odom_y, _odom_theta)
    odom_history.append([_odom_x,_odom_y,_odom_theta])
    np.savetxt(odom_csv_path,odom_history,delimiter=",")

def odometry():
    rospy.init_node('odometry')
    odom_subscriber = rospy.Subscriber('/hsrb/odom', Odometry, callback_odom)
    rospy.spin()

if __name__ == '__main__':
    odometry()
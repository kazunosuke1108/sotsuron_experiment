#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import rospy
from nav_msgs.msg import Odometry   
import tf
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import JointState
import message_filters

from exp_commons import ExpCommons


class OdomSubscriber(ExpCommons):
    def __init__(self):
        super().__init__()
        self.logger=self.prepare_log()
        try:

            try:
                self.topic_name=sys.argv[1]
            except Exception:
                self.topic_name="/hsrb/odom"
            self.topic_joi="/hsrb/joint_states"

            self.frame_id=os.path.basename(os.path.split(self.topic_name)[1])
            self.csv_path=sys.argv[2]+"/"+self.frame_id+"_"+str(sys.argv[3])+".csv"
            rospy.init_node(f"odom_subscriber_{self.frame_id}")
            self.mf=self.pub_sub()
            self.mf.registerCallback(self.OdomCallback)
            rospy.spin()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error(f"line {exc_tb.tb_lineno}: {e}")
            pass


    def pub_sub(self):
        sub_list=[]
        odom_sub=message_filters.Subscriber(self.topic_name, Odometry)
        sub_list.append(odom_sub)
        joi_sub=message_filters.Subscriber(self.topic_joi, JointState)
        sub_list.append(joi_sub)
        mf=message_filters.ApproximateTimeSynchronizer(sub_list,2,1)
        return mf

    def OdomCallback(self,odm_data,joi_data):
        try:
            timestamp = self.get_time(odm_data.header.stamp)
            _odom_x = odm_data.pose.pose.position.x  
            _odom_y = odm_data.pose.pose.position.y  
            qx = odm_data.pose.pose.orientation.x
            qy = odm_data.pose.pose.orientation.y
            qz = odm_data.pose.pose.orientation.z
            qw = odm_data.pose.pose.orientation.w
            q = (qx, qy, qz, qw)
            e = euler_from_quaternion(q)
            _odom_theta = e[2] 

            idx=joi_data.name.index('head_pan_joint')
            pan=joi_data.position[idx]

            output_data=[timestamp,_odom_x,_odom_y,_odom_theta,pan]
            self.write_csvlog(output_data,csvpath=self.csv_path)
            self.logger.info(f"data @ {timestamp} was processed successfully")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error(f"line {exc_tb.tb_lineno}: {e}")
            pass

odomsub=OdomSubscriber()
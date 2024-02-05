#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import rospy
import message_filters
from sensor_msgs.msg import Imu

from exp_commons import ExpCommons


class IMUSubscriber(ExpCommons):
    def __init__(self):
        super().__init__()
        self.logger=self.prepare_log()

        try:
            self.topic_name=sys.argv[1]
        except Exception:
            self.topic_name="/hsrb/base_accurate_imu/data"

        self.frame_id=os.path.basename(os.path.split(self.topic_name)[0])
        self.csv_path=sys.argv[2]+"/"+self.frame_id+"_"+str(sys.argv[3])+".csv"
        rospy.init_node(f"imu_subscriber_{self.frame_id}")
        self.mf=self.pub_sub()
        self.mf.registerCallback(self.ImuCallback)
        rospy.spin()

    def pub_sub(self):
        sub_list=[]
        imu_sub_1=message_filters.Subscriber(self.topic_name,Imu)
        sub_list.append(imu_sub_1)

        mf=message_filters.ApproximateTimeSynchronizer(sub_list,2,1)
        return mf

    def ImuCallback(self,imu_data):
        try:
            output_data=[]
            timestamp=self.get_time(imu_data.header.stamp)
            output_data=output_data+[timestamp]
            orientation=[imu_data.orientation.x,imu_data.orientation.y,imu_data.orientation.z,imu_data.orientation.w]
            output_data=output_data+orientation
            angular_velocity=[imu_data.angular_velocity.x,imu_data.angular_velocity.y,imu_data.angular_velocity.z]
            output_data=output_data+angular_velocity
            linear_acceleration=[imu_data.linear_acceleration.x,imu_data.linear_acceleration.y,imu_data.linear_acceleration.z]
            output_data=output_data+linear_acceleration
            orientation_covariance=imu_data.orientation_covariance
            output_data=output_data+list(orientation_covariance)
            angular_velocity_covariance=imu_data.angular_velocity_covariance
            output_data=output_data+list(angular_velocity_covariance)
            linear_acceleration_covariance=imu_data.linear_acceleration_covariance
            output_data=output_data+list(linear_acceleration_covariance)
            
            self.write_csvlog(output_data,self.csv_path)
            self.logger.info(f"data @ {timestamp} was processed successfully")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error(f"line {exc_tb.tb_lineno}: {e}")
            pass

imusub=IMUSubscriber()
#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import rospy
import message_filters
from geometry_msgs.msg import Twist
from ytlab_nlpmp2_msgs.msg import HsrZr8

from exp_commons import ExpCommons


class HsrZr8Subscriber(ExpCommons):
    def __init__(self):
        super().__init__()
        self.logger=self.prepare_log()
        try:

            try:
                self.topic_name=sys.argv[1]
            except Exception:
                self.topic_name="/HsrZr8"

            self.frame_id=self.topic_name[1:]
            self.csv_path=sys.argv[2]+"/"+self.frame_id+"_"+str(sys.argv[3])+".csv"
            rospy.init_node(f"hsrzr8_subscriber_{self.frame_id}")
            
            rospy.Subscriber(self.topic_name, HsrZr8, self.HsrZr8Callback)
            # self.mf=self.pub_sub()
            # self.mf.registerCallback(self.HsrZr8Callback)
            rospy.spin()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error(f"line {exc_tb.tb_lineno}: {e}")
            pass


    # def pub_sub(self):
    #     sub_list=[]
    #     imu_sub_1=message_filters.Subscriber(self.topic_name,Twist)
    #     sub_list.append(imu_sub_1)

    #     mf=message_filters.ApproximateTimeSynchronizer(sub_list,2,1)
    #     return mf

    def HsrZr8Callback(self,hsrzr8_data):
        try:
            output_data=[]
            timestamp=self.get_time(hsrzr8_data.header.stamp)
            output_data=output_data+[timestamp]
            hsrzr8_info=[hsrzr8_data.x[0],hsrzr8_data.y[0],hsrzr8_data.theta[0],hsrzr8_data.pan[0],hsrzr8_data.v_x[0],hsrzr8_data.v_y[0],hsrzr8_data.omega_theta[0],hsrzr8_data.omega_pan[0]]
            output_data=output_data+hsrzr8_info
            
            self.write_csvlog(output_data,self.csv_path)
            # print(output_data)
            self.logger.info(f"data @ {timestamp} was processed successfully")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error(f"line {exc_tb.tb_lineno}: {e}")
            pass

hsrzr8sub=HsrZr8Subscriber()
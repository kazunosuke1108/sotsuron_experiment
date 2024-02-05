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


from exp_commons import ExpCommons


class TwistSubscriber(ExpCommons):
    def __init__(self):
        super().__init__()
        self.logger=self.prepare_log()
        try:

            try:
                self.topic_name=sys.argv[1]
            except Exception:
                self.topic_name="/hsrb/command_velocity"

            self.frame_id=os.path.basename(os.path.split(self.topic_name)[1])
            self.csv_path=sys.argv[2]+"/"+self.frame_id+"_"+str(sys.argv[3])+".csv"
            rospy.init_node(f"imu_subscriber_{self.frame_id}")
            self.mf=self.pub_sub()
            self.mf.registerCallback(self.TwistCallback)
            rospy.spin()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error(f"line {exc_tb.tb_lineno}: {e}")
            pass


    def pub_sub(self):
        sub_list=[]
        imu_sub_1=message_filters.Subscriber(self.topic_name,Twist)
        sub_list.append(imu_sub_1)

        mf=message_filters.ApproximateTimeSynchronizer(sub_list,2,1)
        return mf

    def ImuCallback(self,twist_data):
        try:
            output_data=[]
            timestamp=self.get_time(twist_data.header.stamp)
            output_data=output_data+[timestamp]
            twist_info=[twist_data.linear.x,twist_data.linear.y,twist_data.linear.z,twist_data.angular.x,twist_data.angular.y,twist_data.angular.z]
            output_data=output_data+twist_info
            
            # self.write_csvlog(output_data,self.csv_path)
            print(output_data)
            self.logger.info(f"data @ {timestamp} was processed successfully")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error(f"line {exc_tb.tb_lineno}: {e}")
            pass

twistsub=TwistSubscriber()
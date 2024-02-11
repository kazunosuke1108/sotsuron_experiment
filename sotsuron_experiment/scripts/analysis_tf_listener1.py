#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from datetime import datetime
from glob import glob
import numpy as np
import pandas as pd

import rospy
import tf
from exp_commons import ExpCommons
# from noise_processor import *

class TfListener(ExpCommons):
    def __init__(self):
        
        # ROS関連
        rospy.init_node("TF_listener")
        # self.rate=rospy.Rate(15)
        self.listener= tf.TransformListener()
        
        # ファイルの立ち上げ
        self.tfrawcsvpath="/home/hayashide/catkin_ws/src/sotsuron_experiment/analysis/velocity_error"+"/"+f"{sys.argv[1]}_odom_to_hmn_01x.csv"
        # self.tfrawcsvpath="/home/hayashide/catkin_ws/src/ytlab_nlpmp_modules/scripts/exp_debug_tf.csv"
        # self.tfprcdcsvpath=self.tfrawcsvpath[:-6]+"prcd.csv"
        # self.tfprcdcsvpath="/home/hayashide/catkin_ws/src/ytlab_nlpmp_modules/scripts/exp_debug_tf_prcd.csv"
        self.rawdata=np.array([])

    def main(self):
        while not rospy.is_shutdown():
            try:
                # odometry
                # TF
                (trans,rot) = self.listener.lookupTransform('/odom', '/hmn_trunk', rospy.Time(0))
                timestamp = self.get_now()
                trans=np.block([np.array(timestamp),np.array(trans)])
                trans=np.array(trans)
                if len(self.rawdata>0):
                    if abs(self.rawdata[-1,1]-trans[1])<1e-4:
                        continue
                    if trans[3]<0:
                        continue
                    self.rawdata=np.block([[self.rawdata],[trans]])
                    pass
                else:
                    # trans=np.block([trans,-0.6,0,0])
                    self.rawdata=[trans]
                self.rawdata=np.array(self.rawdata)
                self.write_csvlog(trans,self.tfrawcsvpath)
                # # np.savetxt(self.tfrawcsvpath,self.rawdata,delimiter=",")
                # if len(self.rawdata)>2:
                #     self.prcddata=initial_processor(pd.DataFrame(self.rawdata,columns=["timestamp","trunk_x","trunk_y","trunk_z"]),denoise=True)
                #     np.savetxt(self.tfprcdcsvpath,self.prcddata,delimiter=",")
                # self.rate.sleep()
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
                # self.rate.sleep()
                continue
        pass

if __name__ == '__main__':
    tf_listener=TfListener()
    tf_listener.main()
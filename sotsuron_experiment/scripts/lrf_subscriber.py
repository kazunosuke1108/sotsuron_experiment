#! /usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import rospy 
import os
from nav_msgs.msg import Odometry   
from sensor_msgs.msg import LaserScan
import message_filters

import tf
import tf2_msgs.msg
import geometry_msgs.msg
from tf.transformations import euler_from_quaternion
import time

class LrfSubscriber():
    def __init__(self):
        rospy.init_node("lrf_subscriber")
        self.mf=self.pub_sub()

        self.img_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/lrf.png"
        self.prediction_csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/dev_lrf/predictions_history.csv"

        self._odom_x, self._odom_y, self._odom_theta = 0.0, 0.0, 0.0
        self.flag_first=True
        self.scan_count=0
        self.black_list_candidate=np.array([])
        self.black_list=np.array([])
        self.prediction_history=[]

    def get_positions(self,msg_scan,x,y,th):
        idx=np.arange(len(msg_scan.ranges))
        rad=msg_scan.angle_min+msg_scan.angle_increment*idx
        xR=x+msg_scan.ranges*np.cos(rad+th)
        yR=y+msg_scan.ranges*np.sin(rad+th)
        return np.array([xR,yR]).T

    def get_walls(self,msg_scan,positions):
        idx=np.arange(len(msg_scan.ranges))
        rad=np.array(msg_scan.angle_min+msg_scan.angle_increment*idx)
        r_idx=np.where((rad>-np.pi/2) & (rad<-np.arctan(2/30)) & (np.array(msg_scan.ranges)<30))
        l_idx=np.where((rad<np.pi/2) & (rad>np.arctan(2/30)) & (np.array(msg_scan.ranges)<30))
        plt.scatter(positions[r_idx,0],positions[r_idx,1],s=0.5,c='r')
        plt.scatter(positions[l_idx,0],positions[l_idx,1],s=0.5,c='r')
        print(positions[r_idx,0][0])
        r_a,r_b=np.polyfit(positions[r_idx,0][0],positions[r_idx,1][0],1)
        l_a,l_b=np.polyfit(positions[l_idx,0][0],positions[l_idx,1][0],1)
        plt.plot([0,30],[r_b,r_a*30+r_b],color="r")
        plt.plot([0,30],[l_b,l_a*30+l_b],color="r")

    # def idx_to_dist(msg_scan,idx1,idx2):
    #     pos1=get_positions(msg_scan,idx1)
    #     pos2=get_positions(msg_scan,idx2)
    #     dist=np.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
    #     return dist

    def pub_sub(self):
        # subscriber
        self.sub_list=[]
        self.odom_sub = message_filters.Subscriber('/hsrb/odom', Odometry)
        self.sub_list.append(self.odom_sub)
        self.scan_sub = message_filters.Subscriber('/teleop_scenario/merged_scan', LaserScan)
        self.sub_list.append(self.scan_sub)

        self.mf=message_filters.ApproximateTimeSynchronizer(self.sub_list,10,0.5)
        self.pub_tf=rospy.Publisher("/tf",tf2_msgs.msg.TFMessage,queue_size=1)
        
        # publisher
        # pub_PointStamped=rospy.Publisher("publisher_point",PointStamped,queue_size=1)

        # listener
        # broadcaster
        return self.mf

    def Callback(self,msg_odom,msg_scan):
        self._odom_x = msg_odom.pose.pose.position.x  
        self._odom_y = msg_odom.pose.pose.position.y  
        self.qx = msg_odom.pose.pose.orientation.x
        self.qy = msg_odom.pose.pose.orientation.y
        self.qz = msg_odom.pose.pose.orientation.z
        self.qw = msg_odom.pose.pose.orientation.w
        self.q = (self.qx, self.qy, self.qz, self.qw)
        self.e = euler_from_quaternion(self.q)
        self._odom_theta = self.e[2] 
        # rospy.loginfo("Odomery: x=%s y=%s theta=%s", _odom_x, _odom_y, _odom_theta)

        # Scan

            

        self.ranges=msg_scan.ranges
        self.positions=self.get_positions(msg_scan,self._odom_x,self._odom_y,self._odom_theta)
        # self.positions[np.isnan(self.positions)]=999
        # self.positions[np.isposinf(self.positions)]=999
        # self.positions[np.isneginf(self.positions)]=999
    
        if self.flag_first:
            self.previous_positions=self.positions
            self.first_positions=self.positions
            # self.previous_positions[np.isnan(self.previous_positions)]=999
            # self.previous_positions[np.isposinf(self.previous_positions)]=999
            # self.previous_positions[np.isneginf(self.previous_positions)]=999
            # self.first_positions[np.isnan(self.first_positions)]=999
            # self.first_positions[np.isposinf(self.first_positions)]=999
            # self.first_positions[np.isneginf(self.first_positions)]=999
            self.flag_first=False
        # print(self.positions-self.previous_positions)
        roi_row=np.unique(np.argwhere((abs(self.positions-self.previous_positions)>0.3) & (abs(self.positions-self.first_positions)>0.3))[:,0])
        
        if self.scan_count%200==0:
            self.scan_count=0
            self.black_list_candidate=np.array([])

        if self.scan_count<100:
            self.black_list_candidate=np.append(self.black_list_candidate,roi_row)
        elif self.scan_count==100:
            black_list_candidate_unique=np.unique(self.black_list_candidate)
            for candidate in black_list_candidate_unique:
                count=np.count_nonzero(self.black_list_candidate==candidate)
                print(count)
                if count>3:
                    self.black_list=np.append(self.black_list,int(candidate))
            rospy.loginfo("###### black list determined ######")
            rospy.loginfo("###### black list determined ######")
            rospy.loginfo(self.black_list)
            rospy.loginfo("###### black list determined ######")
            rospy.loginfo("###### black list determined ######")
        
        t_list=[]
        t_list_idx=[]
        # rospy.loginfo(len(roi_row))
        for idx in roi_row:
            if abs(self.positions[idx][0])>20 or abs(self.positions[idx][1])>20 or (idx in self.black_list):
                continue
            # else:
            #     t_list_idx.append(idx)
            pos=self.positions[idx]
            tf_name=f"foot_candidate_{str(idx+1).zfill(3)}"
            t = geometry_msgs.msg.TransformStamped()
            # t.header.frame_id = "zed_left"
            t.header.frame_id = "base_range_sensor_link"
            t.header.stamp = msg_scan.header.stamp#rospy.Time.now()#rgb_data_header_stamp#rospy.Time.now()
            t.child_frame_id = tf_name
            t.transform.translation.x = pos[0]
            t.transform.translation.y = pos[1]
            t.transform.translation.z = 0
            t.transform.rotation.x = 0.0
            t.transform.rotation.y = 0.0
            t.transform.rotation.z = 0.0
            t.transform.rotation.w = 1.0
            t_list.append(t)
        tfm = tf2_msgs.msg.TFMessage(t_list)
        self.pub_tf.publish(tfm)
        self.previous_positions=self.positions
        # try:
        if len(t_list_idx)==0:
            self.scan_count+=1
            pass
        else:
            for idx in t_list_idx:
                if (idx-1 in t_list_idx) or (idx+1 in t_list_idx):
                    t_list_idx.append(idx)
                    t_list_idx.append(idx)
                    t_list_idx.append(idx)
                    if (idx-1 in t_list_idx) and (idx+1 in t_list_idx):
                        t_list_idx.append(idx)
                        t_list_idx.append(idx)

            mean_idx=int(np.mean(np.array([t_list_idx])))
            scan_time=msg_scan.header.stamp
            scan_time_str=str(scan_time.secs) + '.' + str(scan_time.nsecs)
            export_info=np.block([float(scan_time_str),self.positions[mean_idx]])
            print(export_info)
            # except ValueError:
            #     mean_idx=np.nan
            # try:
            # print(self.prediction_history.T)
            # print(export_info.T)
            self.prediction_history.append(export_info)
            # except ValueError:
            #     self.prediction_history=export_info.T
            np.savetxt(self.prediction_csv_path,self.prediction_history,delimiter=",")
            print(self.prediction_history)
            print(mean_idx,self.positions[mean_idx])
        self.scan_count+=1

    def main(self):    
        self.mf.registerCallback(self.Callback)
        rospy.spin()

lrfsub=LrfSubscriber()
lrfsub.main()

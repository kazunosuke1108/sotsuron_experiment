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
        self.ranges_csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/dev_lrf/positions_history.csv"

        self._odom_x, self._odom_y, self._odom_theta = 0.0, 0.0, 0.0
        self.flag_first=True
        self.scan_count=0
        self.black_list_candidate=np.array([])
        self.black_list=np.array([])
        self.positions_history=[]


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
        # self._odom_x = msg_odom.pose.pose.position.x  
        # self._odom_y = msg_odom.pose.pose.position.y  
        # self.qx = msg_odom.pose.pose.orientation.x
        # self.qy = msg_odom.pose.pose.orientation.y
        # self.qz = msg_odom.pose.pose.orientation.z
        # self.qw = msg_odom.pose.pose.orientation.w
        # self.q = (self.qx, self.qy, self.qz, self.qw)
        # self.e = euler_from_quaternion(self.q)
        # self._odom_theta = self.e[2] 
        # rospy.loginfo("Odomery: x=%s y=%s theta=%s", _odom_x, _odom_y, _odom_theta)

        # Scan

            

        self.ranges=msg_scan.ranges
        self.positions=self.get_positions(msg_scan,0,0,0)#_odom_x,_odom_y,_odom_theta)
        
        if self.flag_first:
            self.previous_positions=self.positions
            self.first_positions=self.positions
            self.flag_first=False

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
                    print(self.black_list)
            rospy.loginfo("###### black list determined ######")
            rospy.loginfo("###### black list determined ######")
            rospy.loginfo(self.black_list)
            rospy.loginfo("###### black list determined ######")
            rospy.loginfo("###### black list determined ######")
        
        t_list=[]
        rospy.loginfo(len(roi_row))
        for idx in roi_row:
            if abs(self.positions[idx][1])>20 or idx in self.black_list:
                continue
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

        self.scan_count+=1

    def main(self):    
        self.mf.registerCallback(self.Callback)
        rospy.spin()

lrfsub=LrfSubscriber()
lrfsub.main()
"""
/action_manager_state
/action_state
/attached_object_information
/base_path_plan/status
/base_path_planner/inflated_static_obstacle_map
/client_count
/clock
/collision_environment_map_array
/collision_environment_marker_array
/connected_clients
/current_floor
/depthcloud_encoded
/depthcloud_encoded/compressed
/depthcloud_encoded/compressed/parameter_descriptions
/depthcloud_encoded/compressed/parameter_updates
/depthcloud_encoded/compressedDepth/parameter_descriptions
/depthcloud_encoded/compressedDepth/parameter_updates
/depthcloud_encoded/theora
/depthcloud_encoded/theora/parameter_descriptions
/depthcloud_encoded/theora/parameter_updates
/diagnostics
/diagnostics_agg
/diagnostics_toplevel_state
/heartbeat
/hsrb/align_angle_sensors/status
/hsrb/arm_trajectory_controller/follow_joint_trajectory/status
/hsrb/arm_trajectory_controller/state
/hsrb/base_b_bumper_sensor
/hsrb/base_f_bumper_sensor
/hsrb/base_imu/data
/hsrb/base_magnetic_sensor_1
/hsrb/base_magnetic_sensor_2
/hsrb/base_magnetic_sensor_3
/hsrb/base_magnetic_sensor_4
/hsrb/base_pose
/hsrb/base_scan
/hsrb/battery_info
/hsrb/battery_state
/hsrb/collision_detection_controller/drivers/arm_flex_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/arm_flex_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/arm_flex_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/arm_flex_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/arm_lift_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/arm_lift_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/arm_lift_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/arm_lift_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/arm_roll_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/arm_roll_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/arm_roll_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/arm_roll_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/base_l_drive_wheel_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/base_l_drive_wheel_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/base_l_drive_wheel_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/base_l_drive_wheel_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/base_r_drive_wheel_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/base_r_drive_wheel_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/base_r_drive_wheel_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/base_r_drive_wheel_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/base_roll_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/base_roll_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/base_roll_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/base_roll_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/head_pan_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/head_pan_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/head_pan_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/head_pan_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/head_tilt_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/head_tilt_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/head_tilt_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/head_tilt_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/wrist_flex_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/wrist_flex_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/wrist_flex_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/wrist_flex_joint/settings/Effort/parameter_updates
/hsrb/collision_detection_controller/drivers/wrist_roll_joint/settings/Current/parameter_descriptions
/hsrb/collision_detection_controller/drivers/wrist_roll_joint/settings/Current/parameter_updates
/hsrb/collision_detection_controller/drivers/wrist_roll_joint/settings/Effort/parameter_descriptions
/hsrb/collision_detection_controller/drivers/wrist_roll_joint/settings/Effort/parameter_updates
/hsrb/command_status_led
/hsrb/command_status_led_rgb
/hsrb/diag/battery_check/status
/hsrb/diag/force_torque_sensor_check/status
/hsrb/diag/hand_camera_check/status
/hsrb/diag/head_center_camera_check/status
/hsrb/diag/imu_sensor_check/status
/hsrb/diag/l_stereo_camera_check/status
/hsrb/diag/motor_amp_check/status
/hsrb/diag/r_stereo_camera_check/status
/hsrb/diag/urg_sensor_check/status
/hsrb/diag/usb_io_check/status
/hsrb/diag/xtion_depth_check/status
/hsrb/diag/xtion_point_check/status
/hsrb/diag/xtion_rgb_check/status
/hsrb/diag_interactive/bumper_sensor_check/status
/hsrb/diag_interactive/microphone_check/status
/hsrb/diag_interactive/pressure_sensor_check/status
/hsrb/diag_interactive/speaker_check/status
/hsrb/diag_interactive/status_led_check/status
/hsrb/diagnostics
/hsrb/diagnostics_agg
/hsrb/drive_mode
/hsrb/gradational_color/status
/hsrb/gripper_controller/apply_force/status
/hsrb/gripper_controller/follow_joint_trajectory/status
/hsrb/gripper_controller/grasp/status
/hsrb/head_rgbd_sensor/depth_registered/camera_info
/hsrb/head_rgbd_sensor/depth_registered/image
/hsrb/head_rgbd_sensor/depth_registered/image/compressed/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image/compressed/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image/compressedDepth
/hsrb/head_rgbd_sensor/depth_registered/image/compressedDepth/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image/compressedDepth/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image/theora
/hsrb/head_rgbd_sensor/depth_registered/image/theora/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image/theora/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image_raw
/hsrb/head_rgbd_sensor/depth_registered/image_raw/compressed
/hsrb/head_rgbd_sensor/depth_registered/image_raw/compressed/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image_raw/compressed/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image_raw/compressedDepth
/hsrb/head_rgbd_sensor/depth_registered/image_raw/compressedDepth/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image_raw/compressedDepth/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image_raw/theora
/hsrb/head_rgbd_sensor/depth_registered/image_raw/theora/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image_raw/theora/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/compressed
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/compressed/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/compressed/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/compressedDepth
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/compressedDepth/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/compressedDepth/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/theora
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/theora/parameter_descriptions
/hsrb/head_rgbd_sensor/depth_registered/image_rect_raw/theora/parameter_updates
/hsrb/head_rgbd_sensor/depth_registered/rectified_points
/hsrb/head_rgbd_sensor/driver/parameter_descriptions
/hsrb/head_rgbd_sensor/driver/parameter_updates
/hsrb/head_rgbd_sensor/head_rgbd_sensor_nodelet_manager/bond
/hsrb/head_rgbd_sensor/ir/image/compressed/parameter_descriptions
/hsrb/head_rgbd_sensor/ir/image/compressed/parameter_updates
/hsrb/head_rgbd_sensor/ir/image/compressedDepth/parameter_descriptions
/hsrb/head_rgbd_sensor/ir/image/compressedDepth/parameter_updates
/hsrb/head_rgbd_sensor/ir/image/theora/parameter_descriptions
/hsrb/head_rgbd_sensor/ir/image/theora/parameter_updates
/hsrb/head_rgbd_sensor/projector/camera_info
/hsrb/head_rgbd_sensor/rgb/camera_info
/hsrb/head_rgbd_sensor/rgb/image_raw
/hsrb/head_rgbd_sensor/rgb/image_raw/compressed
/hsrb/head_rgbd_sensor/rgb/image_raw/compressed/parameter_descriptions
/hsrb/head_rgbd_sensor/rgb/image_raw/compressed/parameter_updates
/hsrb/head_rgbd_sensor/rgb/image_raw/compressedDepth/parameter_descriptions
/hsrb/head_rgbd_sensor/rgb/image_raw/compressedDepth/parameter_updates
/hsrb/head_rgbd_sensor/rgb/image_raw/theora
/hsrb/head_rgbd_sensor/rgb/image_raw/theora/parameter_descriptions
/hsrb/head_rgbd_sensor/rgb/image_raw/theora/parameter_updates
/hsrb/head_rgbd_sensor/rgb/image_rect_color
/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressed
/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressed/parameter_descriptions
/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressed/parameter_updates
/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressedDepth/parameter_descriptions
/hsrb/head_rgbd_sensor/rgb/image_rect_color/compressedDepth/parameter_updates
/hsrb/head_rgbd_sensor/rgb/image_rect_color/theora
/hsrb/head_rgbd_sensor/rgb/image_rect_color/theora/parameter_descriptions
/hsrb/head_rgbd_sensor/rgb/image_rect_color/theora/parameter_updates
/hsrb/head_rgbd_sensor/rgb_rectify_color/parameter_descriptions
/hsrb/head_rgbd_sensor/rgb_rectify_color/parameter_updates
/hsrb/head_trajectory_controller/follow_joint_trajectory/status
/hsrb/head_trajectory_controller/state
/hsrb/hsrb_grasp_state_observer/parameter_descriptions
/hsrb/hsrb_grasp_state_observer/parameter_updates
/hsrb/impedance_control/compliance_hard/constraints/cartesian/goal/parameter_descriptions
/hsrb/impedance_control/compliance_hard/constraints/cartesian/goal/parameter_updates
/hsrb/impedance_control/compliance_hard/constraints/cartesian/path/parameter_descriptions
/hsrb/impedance_control/compliance_hard/constraints/cartesian/path/parameter_updates
/hsrb/impedance_control/compliance_hard/impedance/rotation/x/parameter_descriptions
/hsrb/impedance_control/compliance_hard/impedance/rotation/x/parameter_updates
/hsrb/impedance_control/compliance_hard/impedance/rotation/y/parameter_descriptions
/hsrb/impedance_control/compliance_hard/impedance/rotation/y/parameter_updates
/hsrb/impedance_control/compliance_hard/impedance/rotation/z/parameter_descriptions
/hsrb/impedance_control/compliance_hard/impedance/rotation/z/parameter_updates
/hsrb/impedance_control/compliance_hard/impedance/translation/x/parameter_descriptions
/hsrb/impedance_control/compliance_hard/impedance/translation/x/parameter_updates
/hsrb/impedance_control/compliance_hard/impedance/translation/y/parameter_descriptions
/hsrb/impedance_control/compliance_hard/impedance/translation/y/parameter_updates
/hsrb/impedance_control/compliance_hard/impedance/translation/z/parameter_descriptions
/hsrb/impedance_control/compliance_hard/impedance/translation/z/parameter_updates
/hsrb/impedance_control/compliance_hard/output_path/parameter_descriptions
/hsrb/impedance_control/compliance_hard/output_path/parameter_updates
/hsrb/impedance_control/compliance_middle/constraints/cartesian/goal/parameter_descriptions
/hsrb/impedance_control/compliance_middle/constraints/cartesian/goal/parameter_updates
/hsrb/impedance_control/compliance_middle/constraints/cartesian/path/parameter_descriptions
/hsrb/impedance_control/compliance_middle/constraints/cartesian/path/parameter_updates
/hsrb/impedance_control/compliance_middle/impedance/rotation/x/parameter_descriptions
/hsrb/impedance_control/compliance_middle/impedance/rotation/x/parameter_updates
/hsrb/impedance_control/compliance_middle/impedance/rotation/y/parameter_descriptions
/hsrb/impedance_control/compliance_middle/impedance/rotation/y/parameter_updates
/hsrb/impedance_control/compliance_middle/impedance/rotation/z/parameter_descriptions
/hsrb/impedance_control/compliance_middle/impedance/rotation/z/parameter_updates
/hsrb/impedance_control/compliance_middle/impedance/translation/x/parameter_descriptions
/hsrb/impedance_control/compliance_middle/impedance/translation/x/parameter_updates
/hsrb/impedance_control/compliance_middle/impedance/translation/y/parameter_descriptions
/hsrb/impedance_control/compliance_middle/impedance/translation/y/parameter_updates
/hsrb/impedance_control/compliance_middle/impedance/translation/z/parameter_descriptions
/hsrb/impedance_control/compliance_middle/impedance/translation/z/parameter_updates
/hsrb/impedance_control/compliance_middle/output_path/parameter_descriptions
/hsrb/impedance_control/compliance_middle/output_path/parameter_updates
/hsrb/impedance_control/compliance_soft/constraints/cartesian/goal/parameter_descriptions
/hsrb/impedance_control/compliance_soft/constraints/cartesian/goal/parameter_updates
/hsrb/impedance_control/compliance_soft/constraints/cartesian/path/parameter_descriptions
/hsrb/impedance_control/compliance_soft/constraints/cartesian/path/parameter_updates
/hsrb/impedance_control/compliance_soft/impedance/rotation/x/parameter_descriptions
/hsrb/impedance_control/compliance_soft/impedance/rotation/x/parameter_updates
/hsrb/impedance_control/compliance_soft/impedance/rotation/y/parameter_descriptions
/hsrb/impedance_control/compliance_soft/impedance/rotation/y/parameter_updates
/hsrb/impedance_control/compliance_soft/impedance/rotation/z/parameter_descriptions
/hsrb/impedance_control/compliance_soft/impedance/rotation/z/parameter_updates
/hsrb/impedance_control/compliance_soft/impedance/translation/x/parameter_descriptions
/hsrb/impedance_control/compliance_soft/impedance/translation/x/parameter_updates
/hsrb/impedance_control/compliance_soft/impedance/translation/y/parameter_descriptions
/hsrb/impedance_control/compliance_soft/impedance/translation/y/parameter_updates
/hsrb/impedance_control/compliance_soft/impedance/translation/z/parameter_descriptions
/hsrb/impedance_control/compliance_soft/impedance/translation/z/parameter_updates
/hsrb/impedance_control/compliance_soft/output_path/parameter_descriptions
/hsrb/impedance_control/compliance_soft/output_path/parameter_updates
/hsrb/impedance_control/dumper_hard/constraints/cartesian/goal/parameter_descriptions
/hsrb/impedance_control/dumper_hard/constraints/cartesian/goal/parameter_updates
/hsrb/impedance_control/dumper_hard/constraints/cartesian/path/parameter_descriptions
/hsrb/impedance_control/dumper_hard/constraints/cartesian/path/parameter_updates
/hsrb/impedance_control/dumper_hard/impedance/rotation/x/parameter_descriptions
/hsrb/impedance_control/dumper_hard/impedance/rotation/x/parameter_updates
/hsrb/impedance_control/dumper_hard/impedance/rotation/y/parameter_descriptions
/hsrb/impedance_control/dumper_hard/impedance/rotation/y/parameter_updates
/hsrb/impedance_control/dumper_hard/impedance/rotation/z/parameter_descriptions
/hsrb/impedance_control/dumper_hard/impedance/rotation/z/parameter_updates
/hsrb/impedance_control/dumper_hard/impedance/translation/x/parameter_descriptions
/hsrb/impedance_control/dumper_hard/impedance/translation/x/parameter_updates
/hsrb/impedance_control/dumper_hard/impedance/translation/y/parameter_descriptions
/hsrb/impedance_control/dumper_hard/impedance/translation/y/parameter_updates
/hsrb/impedance_control/dumper_hard/impedance/translation/z/parameter_descriptions
/hsrb/impedance_control/dumper_hard/impedance/translation/z/parameter_updates
/hsrb/impedance_control/dumper_hard/output_path/parameter_descriptions
/hsrb/impedance_control/dumper_hard/output_path/parameter_updates
/hsrb/impedance_control/dumper_soft/constraints/cartesian/goal/parameter_descriptions
/hsrb/impedance_control/dumper_soft/constraints/cartesian/goal/parameter_updates
/hsrb/impedance_control/dumper_soft/constraints/cartesian/path/parameter_descriptions
/hsrb/impedance_control/dumper_soft/constraints/cartesian/path/parameter_updates
/hsrb/impedance_control/dumper_soft/impedance/rotation/x/parameter_descriptions
/hsrb/impedance_control/dumper_soft/impedance/rotation/x/parameter_updates
/hsrb/impedance_control/dumper_soft/impedance/rotation/y/parameter_descriptions
/hsrb/impedance_control/dumper_soft/impedance/rotation/y/parameter_updates
/hsrb/impedance_control/dumper_soft/impedance/rotation/z/parameter_descriptions
/hsrb/impedance_control/dumper_soft/impedance/rotation/z/parameter_updates
/hsrb/impedance_control/dumper_soft/impedance/translation/x/parameter_descriptions
/hsrb/impedance_control/dumper_soft/impedance/translation/x/parameter_updates
/hsrb/impedance_control/dumper_soft/impedance/translation/y/parameter_descriptions
/hsrb/impedance_control/dumper_soft/impedance/translation/y/parameter_updates
/hsrb/impedance_control/dumper_soft/impedance/translation/z/parameter_descriptions
/hsrb/impedance_control/dumper_soft/impedance/translation/z/parameter_updates
/hsrb/impedance_control/dumper_soft/output_path/parameter_descriptions
/hsrb/impedance_control/dumper_soft/output_path/parameter_updates
/hsrb/impedance_control/follow_joint_trajectory/status
/hsrb/impedance_control/follow_joint_trajectory_with_config/status
/hsrb/impedance_control/grasping/constraints/cartesian/goal/parameter_descriptions
/hsrb/impedance_control/grasping/constraints/cartesian/goal/parameter_updates
/hsrb/impedance_control/grasping/constraints/cartesian/path/parameter_descriptions
/hsrb/impedance_control/grasping/constraints/cartesian/path/parameter_updates
/hsrb/impedance_control/grasping/impedance/rotation/x/parameter_descriptions
/hsrb/impedance_control/grasping/impedance/rotation/x/parameter_updates
/hsrb/impedance_control/grasping/impedance/rotation/y/parameter_descriptions
/hsrb/impedance_control/grasping/impedance/rotation/y/parameter_updates
/hsrb/impedance_control/grasping/impedance/rotation/z/parameter_descriptions
/hsrb/impedance_control/grasping/impedance/rotation/z/parameter_updates
/hsrb/impedance_control/grasping/impedance/translation/x/parameter_descriptions
/hsrb/impedance_control/grasping/impedance/translation/x/parameter_updates
/hsrb/impedance_control/grasping/impedance/translation/y/parameter_descriptions
/hsrb/impedance_control/grasping/impedance/translation/y/parameter_updates
/hsrb/impedance_control/grasping/impedance/translation/z/parameter_descriptions
/hsrb/impedance_control/grasping/impedance/translation/z/parameter_updates
/hsrb/impedance_control/grasping/output_path/parameter_descriptions
/hsrb/impedance_control/grasping/output_path/parameter_updates
/hsrb/impedance_control/placing/constraints/cartesian/goal/parameter_descriptions
/hsrb/impedance_control/placing/constraints/cartesian/goal/parameter_updates
/hsrb/impedance_control/placing/constraints/cartesian/path/parameter_descriptions
/hsrb/impedance_control/placing/constraints/cartesian/path/parameter_updates
/hsrb/impedance_control/placing/impedance/rotation/x/parameter_descriptions
/hsrb/impedance_control/placing/impedance/rotation/x/parameter_updates
/hsrb/impedance_control/placing/impedance/rotation/y/parameter_descriptions
/hsrb/impedance_control/placing/impedance/rotation/y/parameter_updates
/hsrb/impedance_control/placing/impedance/rotation/z/parameter_descriptions
/hsrb/impedance_control/placing/impedance/rotation/z/parameter_updates
/hsrb/impedance_control/placing/impedance/translation/x/parameter_descriptions
/hsrb/impedance_control/placing/impedance/translation/x/parameter_updates
/hsrb/impedance_control/placing/impedance/translation/y/parameter_descriptions
/hsrb/impedance_control/placing/impedance/translation/y/parameter_updates
/hsrb/impedance_control/placing/impedance/translation/z/parameter_descriptions
/hsrb/impedance_control/placing/impedance/translation/z/parameter_updates
/hsrb/impedance_control/placing/output_path/parameter_descriptions
/hsrb/impedance_control/placing/output_path/parameter_updates
/hsrb/joint_impedance_control_server/arm_flex_joint/parameter_descriptions
/hsrb/joint_impedance_control_server/arm_flex_joint/parameter_updates
/hsrb/joint_impedance_control_server/base_roll_joint/parameter_descriptions
/hsrb/joint_impedance_control_server/base_roll_joint/parameter_updates
/hsrb/joint_states
/hsrb/laser_odom
/hsrb/odom
/hsrb/omni_base_controller/command
/hsrb/omni_base_controller/follow_joint_trajectory/status
/hsrb/omni_base_controller/internal_state
/hsrb/omni_base_controller/state
/hsrb/overload_joint_state
/hsrb/pose2D
/hsrb/pressure_sensor
/hsrb/robot_state/joint_states
/hsrb/runstop_button
/hsrb/servo_states
/hsrb/suction_control/status
/hsrb/urg_node/parameter_descriptions
/hsrb/urg_node/parameter_updates
/hsrb/wheel_odom
/hsrb_timeopt_filter/parameter_descriptions
/hsrb_timeopt_filter/parameter_updates
/hsrb_timeopt_filter_node/parameter_descriptions
/hsrb_timeopt_filter_node/parameter_updates
/known_object_ids
/laser_2d_localizer/score
/laser_2d_particles
/laser_2d_pose
/laser_2d_pose_ref
/marker/parameter_descriptions
/marker/parameter_updates
/move_base/move/status
/path_follow_action/status
/rosout
/rosout_agg
/static_distance_map
/static_distance_map_ref
/static_distance_ros_map
/static_obstacle_map
/static_obstacle_map_ref
/static_obstacle_ros_map
/talk_request_action/status
/talking_sentence
/tf
/tf2_buffer_server/status
/tf2_web_republisher/status
/tf_static
/tmc_map_merger/inputs/base_scan/obstacle_circle/parameter_descriptions
/tmc_map_merger/inputs/base_scan/obstacle_circle/parameter_updates
/tmc_map_merger/inputs/base_scan/parameter_descriptions
/tmc_map_merger/inputs/base_scan/parameter_updates
/tmc_map_merger/inputs/head_rgbd_sensor/obstacle_circle/parameter_descriptions
/tmc_map_merger/inputs/head_rgbd_sensor/obstacle_circle/parameter_updates
/tmc_map_merger/inputs/head_rgbd_sensor/parameter_descriptions
/tmc_map_merger/inputs/head_rgbd_sensor/parameter_updates
/tmc_remote_exec/run/status
/urg_cloud

"""
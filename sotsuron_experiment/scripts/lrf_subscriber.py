#! /usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import rospy 
import os
from nav_msgs.msg import Odometry   
import tf
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped
import message_filters
csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/monitor/lrf.csv"
ranges_csv_path=os.environ['HOME']+"/catkin_ws/src/sotsuron_experiment/scripts/sources/ranges.csv"

_odom_x, _odom_y, _odom_theta = 0.0, 0.0, 0.0
footcandidate=[]
footcandidate_idx=[]
footcandidate2=[]
footcandidate2_idx=[]
footcandidate3=[]
footcandidate3_idx=[]
footcandidate4=[]
footcandidate4_idx=[]
yorozu_idx=[]

def idx_to_pos(msg_scan,idx):
    rad=msg_scan.angle_min+msg_scan.angle_increment*idx
    xR=msg_scan.ranges[idx]*np.cos(rad)
    yR=msg_scan.ranges[idx]*np.sin(rad)
        
            
    return np.array([xR,yR]).T

def idx_to_dist(msg_scan,idx1,idx2):
    pos1=idx_to_pos(msg_scan,idx1)
    pos2=idx_to_pos(msg_scan,idx2)
    dist=np.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)
    return dist

def pub_sub():
    global rgb_sub,dpt_sub,info_sub,pub_PointStamped
    # subscriber
    sub_list=[]
    odom_sub = message_filters.Subscriber('/hsrb/odom', Odometry)
    sub_list.append(odom_sub)
    scan_sub = message_filters.Subscriber('/hsrb/base_scan', LaserScan)
    sub_list.append(scan_sub)

    mf=message_filters.ApproximateTimeSynchronizer(sub_list,10,0.5)
    
    # publisher
    pub_PointStamped=rospy.Publisher("publisher_point",PointStamped,queue_size=1)

    # listener

    # broadcaster

    return mf

def Callback(msg_odom,msg_scan):
    # Odometory
    global _odom_x, _odom_y, _odon_theta 
    _odom_x = msg_odom.pose.pose.position.x  
    _odom_y = msg_odom.pose.pose.position.y  
    qx = msg_odom.pose.pose.orientation.x
    qy = msg_odom.pose.pose.orientation.y
    qz = msg_odom.pose.pose.orientation.z
    qw = msg_odom.pose.pose.orientation.w
    q = (qx, qy, qz, qw)
    e = euler_from_quaternion(q)
    _odom_theta = e[2] 
    # rospy.loginfo("Odomery: x=%s y=%s theta=%s", _odom_x, _odom_y, _odom_theta)

    # Scan
    ranges=msg_scan.ranges
    # rospy.loginfo(f"max:{max(ranges)}, min:{min(ranges)}")

    np.savetxt(ranges_csv_path,ranges,delimiter=",")

    point=PointStamped()
    point.header.stamp=rospy.Time.now()
    point.header.frame_id="base_link"
    # pos=idx_to_pos(msg_scan,idx-1)
    point.point.x=0
    point.point.y=0
    point.point.z=0
    # rospy.loginfo(point)
    pub_PointStamped.publish(point)

    # original_candidate=[]
    # for i in range(1,len(ranges)):
    #     if abs(ranges[i]-ranges[i-1])>=1.0:
    #         # エッジ認定
    #         original_candidate.append([ranges[i],i])
    
    # print(len(original_candidate))
    # for i,data in enumerate(original_candidate):
    #     idx=data[1]
    #     point=PointStamped()
    #     point.header.stamp=rospy.Time.now()
    #     point.header.frame_id="base_link"
    #     pos=idx_to_pos(msg_scan,idx-1)
    #     point.point.x=pos[0]
    #     point.point.y=pos[1]
    #     point.point.z=0
    #     # rospy.loginfo(point)
    #     pub_PointStamped.publish(point)

    # yorozu method
    edge_list=[]
    a_list=[]
    b_list=[]
    candidate_list=[]
    # for i in range(1,len(ranges)):
    #     if abs(ranges[i]-ranges[i-1])>0.1:
    #         # エッジ認定
    #         edge_list.append([ranges[i],i])

    # for i in range(3,len(edge_list)):
    #     if idx_to_dist(msg_scan,i,i-1)>0.01 and idx_to_dist(msg_scan,i,i-1)<0.2 and idx_to_dist(msg_scan,i-2,i-3)>0.01 and idx_to_dist(msg_scan,i-2,i-3)<0.2:
    #         # a条件クリア・柱認定
    #         a_list.append(ranges.index(edge_list[i][0]))
    #         left_idx=int((edge_list[i][1]+edge_list[i-1][1])/2)
    #         right_idx=int((edge_list[i-2][1]+edge_list[i-3][1])/2)
    #         dist=idx_to_dist(msg_scan,left_idx,right_idx)
    #         if dist>0.1 and dist<1.0:
    #             # b条件クリア・2本の柱認定
    #             b_list.append(ranges.index(edge_list[i][0]))
    #             feetwidth=idx_to_dist(msg_scan,i,i-3)
    #             if feetwidth>0.2 and feetwidth<0.4:
    #                 # c条件クリア・足全体認定
    #                 candidate_list.append(ranges.index(edge_list[i][0]))
    #                 pass

    # for i in range(1,len(ranges)):
    #     if abs(ranges[i]-ranges[i-1])>=0:
    #         # エッジ認定
    #         edge_list.append([ranges[i],i])

    # for i in range(3,len(edge_list)):
    #     if idx_to_dist(msg_scan,i,i-1)>0.001 and idx_to_dist(msg_scan,i,i-1)<100 and idx_to_dist(msg_scan,i-2,i-3)>0.001 and idx_to_dist(msg_scan,i-2,i-3)<100.0:
    #         # a条件クリア・柱が**隣接して**2つある認定
    #         a_list.append(ranges.index(edge_list[i][0]))
    #         left_idx=int((edge_list[i][1]+edge_list[i-1][1])/2)
    #         right_idx=int((edge_list[i-2][1]+edge_list[i-3][1])/2)
    #         dist=idx_to_dist(msg_scan,left_idx,right_idx)
    #         if dist>0.01 and dist<3.0:
    #             # b条件クリア・2本の柱認定
    #             b_list.append(ranges.index(edge_list[i][0]))
    #             feetwidth=idx_to_dist(msg_scan,i,i-3)
    #             if feetwidth>0.2 and feetwidth<0.4:
    #                 # c条件クリア・足全体認定
    #                 candidate_list.append(ranges.index(edge_list[i][0]))
    #                 pass
    # for i,idx in enumerate(candidate_list):
    #     point=PointStamped()
    #     point.header.stamp=rospy.Time.now()
    #     point.header.frame_id="base_link"
    #     pos=idx_to_pos(msg_scan,idx-1)
    #     point.point.x=pos[0]
    #     point.point.y=pos[1]
    #     point.point.z=0
    #     # rospy.loginfo(point)
    #     pub_PointStamped.publish(point)
    # print(f"{len(edge_list)} -> {len(a_list)} -> {len(b_list)} -> {len(candidate_list)}")
    # yorozu_idx.append(candidate_list)
    # print(candidate_list)












    # # 2d func assumption
    # win=15
    # err_list=[]
    # for i in range(len(ranges)-win):
    #     ranges_roi=np.array(ranges[i:i+win])
    #     if np.average(ranges_roi)>20:
    #         err_list.append(9999)
    #         continue
    #     ranges_norm=(ranges_roi-min(ranges_roi))/(max(ranges_roi)-min(ranges_roi))
    #     indexes=np.arange(-1,1,2/win)
    #     a,b,c=np.polyfit(indexes,ranges_norm,2)
    #     if a<0:
    #         err_list.append(999)
    #         continue
    #     estm=a*ranges_norm**2+b*ranges_norm+c
    #     err=np.average(ranges_norm-estm)
    #     err_list.append(abs(err))

    # err_sorted=sorted(err_list)
    # footcandidate.append(ranges[err_list.index(err_sorted[0])+int(win/2)])
    # footcandidate_idx.append(err_list.index(err_sorted[0]))
    # footcandidate2.append(ranges[err_list.index(err_sorted[1])]+int(win/2))
    # footcandidate2_idx.append(err_list.index(err_sorted[1]))
    # savemtx=np.column_stack((np.array(footcandidate).T,np.array(footcandidate_idx).T,np.array(footcandidate2).T,np.array(footcandidate2_idx).T))
    # np.savetxt(csv_path,savemtx,delimiter=",")
    # rospy.loginfo(f"{err_list.index(min(err_list))} {min(err_list)}")

    
rospy.init_node("lrf_subscriber")
mf=pub_sub()
mf.registerCallback(Callback)
rospy.spin()

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
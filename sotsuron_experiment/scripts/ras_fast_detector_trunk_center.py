#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime
import numpy as np
import cv2
from cv_bridge import CvBridge
import sys

import rospy
import message_filters
from sensor_msgs.msg import Image,CameraInfo
import geometry_msgs.msg
import tf2_msgs.msg

from detectron2_core import *


class bdboxDetector():
    def __init__(self):
        self.logger=self.prepare_log()
        # ROS
        rospy.init_node('ras_fast_detector')
        # parameters
        self.rotation=True
        self.model_type="KP"

        # path
        # try:
        #     self.logcsvpath=sys.argv[1]
        # except Exception:
        self.logcsvpath="/home/hayashide/catkin_ws/src/sotsuron_experiment/exp_log/fast_detector"+"/"+datetime.now().strftime('%Y%m%d_%H%M%S')+".csv"
        
        self.tf2d_csvpath=sys.argv[1]

        # Detectron2
        self.detector=Detector(model_type=self.model_type)

        # name
        # self.topic_img_hsr="/stereo/left/image_rect"
        # self.topic_dpt_hsr="/stereo/depth"
        # self.topic_info_hsr="/stereo/left/camera_info"
        # self.frame_hsr="zed_left_optical"
        self.topic_rgb_zed="/zed/zed_node/rgb/image_rect_color"
        self.topic_gry_zed="/zed/zed_node/rgb/image_rect_gray"
        self.topic_dpt_zed="/zed/zed_node/depth/depth_registered"
        self.topic_info_zed="/zed/zed_node/rgb/camera_info"
        self.frame_zed="zed_left_camera_optical_frame"
        self.frame_zed_calib="zed_left_camera_optical_frame_calib"
        self.frame_zed_tate="zed_left_camera_optical_frame_tate"


        # preparation
        self.mf=self.pub_sub()
        self.mf.registerCallback(self.ImageCallback)
        rospy.spin()

    def get_time(self,rostime=None):
        if rostime==None:
            rostime=rospy.Time.now()
        ans=float(str(rostime.secs)+"."+format(rostime.nsecs,'09'))
        # ans=time.time()
        return ans

    def prepare_log(self):
        import os
        from datetime import datetime
        import logging

        # logdir=os.path.split(os.path.split(__file__)[0])[0]+"/log"
        logdir = "/home/hayashide/catkin_ws/src/sotsuron_experiment/log"
        logdaydir=logdir+"/"+datetime.now().strftime('%Y%m%d')
        os.makedirs(logdaydir,exist_ok=True)

        logger = logging.getLogger(os.path.basename(__file__))
        logger.setLevel(logging.DEBUG)
        format = "%(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(levelname)-9s  %(message)s"
        st_handler = logging.StreamHandler()
        st_handler.setLevel(logging.DEBUG)
        # StreamHandlerによる出力フォーマットを先で定義した'format'に設定
        st_handler.setFormatter(logging.Formatter(format))

        fl_handler = logging.FileHandler(filename=logdaydir+"/"+datetime.now().strftime('%Y%m%d_%H%M%S')+".log", encoding="utf-8")
        fl_handler.setLevel(logging.INFO)
        # FileHandlerによる出力フォーマットを先で定義した'format'に設定
        fl_handler.setFormatter(logging.Formatter(format))

        logger.addHandler(st_handler)
        logger.addHandler(fl_handler)
        return logger
    
    def pub_sub(self):
        sub_list=[]
        rgb_sub=message_filters.Subscriber(self.topic_rgb_zed,Image)
        sub_list.append(rgb_sub)
        dpt_sub=message_filters.Subscriber(self.topic_dpt_zed,Image)
        sub_list.append(dpt_sub)
        info_sub=message_filters.Subscriber(self.topic_info_zed,CameraInfo)
        sub_list.append(info_sub)
        self.mf=message_filters.ApproximateTimeSynchronizer(sub_list,2,1)

        self.pub_tf=rospy.Publisher("/tf",tf2_msgs.msg.TFMessage,queue_size=1)

        return self.mf
    
    def get_image(self,data,datatype="rgb_ZED"):
        data_time=self.get_time(data.header.stamp)
        if datatype=="rgb_ZED":
            rgb_array = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
            rgb_array=np.nan_to_num(rgb_array, copy=False)
            rgb_array=cv2.cvtColor(rgb_array,cv2.COLOR_BGR2RGB)
            return rgb_array
        elif datatype=="dpt":
            dpt_array=CvBridge().imgmsg_to_cv2(data)
            dpt_array=np.array(dpt_array,dtype=np.float32)            
            return dpt_array
    
    def get_position(self,rgb_array,dpt_array,proj_mtx):
        def detect_kp(rgb_array):
            if self.rotation:
                rgb_array_t=cv2.rotate(rgb_array,cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                rgb_array_t=rgb_array
            
            pred_keypoints_t=self.detector.onImage(image_mat=rgb_array_t)
            try:
                np_pred_keypoints_t=pred_keypoints_t.to(torch.device('cpu')).detach().clone().numpy()[0]
                np_pred_keypoints_t=np_pred_keypoints_t.astype('int32')
                if self.rotation:
                    np_pred_keypoints=np.zeros_like(np_pred_keypoints_t)
                    np_pred_keypoints[:,1]=np_pred_keypoints_t[:,0]
                    np_pred_keypoints[:,0]=rgb_array.shape[1]-np_pred_keypoints_t[:,1]
                else:
                    np_pred_keypoints=np_pred_keypoints_t
                output_np_pred_keypoints=np_pred_keypoints.flatten()
                output_np_pred_keypoints=output_np_pred_keypoints.astype(np.float128)
                output_np_pred_keypoints=np.insert(output_np_pred_keypoints,0,self.get_time())
                self.write_log(output_np_pred_keypoints,csvpath=self.tf2d_csvpath)
                return np_pred_keypoints
            
            except IndexError:
                return [None]    
        def get_position_kp(rgb_array,dpt_array,np_pred_keypoints,proj_mtx):
            # size translation
            y_rgb2dpt=dpt_array.shape[0]/rgb_array.shape[0]
            x_rgb2dpt=dpt_array.shape[1]/rgb_array.shape[1]

            pred_keypoints_3D=[]

            for i, kp in enumerate(np_pred_keypoints):
                kp_0=int(kp[0]*y_rgb2dpt)
                kp_1=int(kp[1]*x_rgb2dpt)
                size_bdbox=5
                bdbox_0_min=np.max([0,int(kp_1)-size_bdbox])
                bdbox_0_max=np.min([dpt_array.shape[0],int(kp_1)+size_bdbox])
                bdbox_1_min=np.max([0,int(kp_0)-size_bdbox])
                bdbox_1_max=np.min([dpt_array.shape[1],int(kp_0)+size_bdbox])
                dpt=np.nanmin(dpt_array[bdbox_0_min:bdbox_0_max,bdbox_1_min:bdbox_1_max])
                kp_3d=dpt*np.dot(np.linalg.pinv(proj_mtx),np.array([kp_0,kp_1,1]).T)
                pred_keypoints_3D.append(kp_3d.tolist())
            np_pred_keypoints_3D=np.array(pred_keypoints_3D)
            return np_pred_keypoints_3D
            
        def get_gravity_zone(np_pred_keypoints_3D):
            mass={
                "head":0.044,
                "neck":0.033,
                "body":0.479,
                "upper_arm":0.0265,
                "lower_arm":0.015,
                "hand":0.009,
                "upper_leg":0.1,
                "lower_leg":0.0535,
                "foot":0.019
            }
            total_mass=mass["head"]+mass["neck"]+mass["body"]+2*(mass["upper_arm"]+mass["lower_arm"]+mass["hand"]+mass["upper_leg"]+mass["lower_leg"]+mass["foot"])
            position={
                "head":1/5*(np_pred_keypoints_3D[0]+np_pred_keypoints_3D[1]+np_pred_keypoints_3D[2]+np_pred_keypoints_3D[3]+np_pred_keypoints_3D[4]),
                "neck":1/3*(np_pred_keypoints_3D[0]+np_pred_keypoints_3D[1]+np_pred_keypoints_3D[2]),
                "body":1/4*(np_pred_keypoints_3D[5]+np_pred_keypoints_3D[6]+np_pred_keypoints_3D[11]+np_pred_keypoints_3D[12]),
                "upper_arm_L":1/2*(np_pred_keypoints_3D[5]+np_pred_keypoints_3D[7]),
                "upper_arm_R":1/2*(np_pred_keypoints_3D[6]+np_pred_keypoints_3D[8]),
                "lower_arm_L":1/2*(np_pred_keypoints_3D[7]+np_pred_keypoints_3D[9]),
                "lower_arm_R":1/2*(np_pred_keypoints_3D[8]+np_pred_keypoints_3D[10]),
                "hand_L":np_pred_keypoints_3D[9],
                "hand_R":np_pred_keypoints_3D[10],
                "upper_leg_L":1/2*(np_pred_keypoints_3D[11]+np_pred_keypoints_3D[13]),
                "upper_leg_R":1/2*(np_pred_keypoints_3D[12]+np_pred_keypoints_3D[14]),
                "lower_leg_L":1/2*(np_pred_keypoints_3D[13]+np_pred_keypoints_3D[15]),
                "lower_leg_R":1/2*(np_pred_keypoints_3D[14]+np_pred_keypoints_3D[16]),
                "foot_L":np_pred_keypoints_3D[15],
                "foot_R":np_pred_keypoints_3D[16]
            }
            part_gravity={
                "head":mass['head']*position['head'],
                "neck":mass['neck']*position['neck'],
                "body":mass['body']*position['body'],
                "upper_arm":mass['upper_arm']*(position['upper_arm_L']+position['upper_arm_R']),
                "lower_arm":mass['lower_arm']*(position['lower_arm_L']+position['lower_arm_R']),
                "hand":mass['hand']*(position['hand_L']+position['hand_R']),
                "upper_leg":mass['upper_leg']*(position['upper_leg_L']+position['upper_leg_R']),
                "lower_leg":mass['lower_leg']*(position['lower_leg_L']+position['lower_leg_R']),
                "foot":mass['foot']*(position['foot_L']+position['foot_R'])
            }

            gravity_zone=1/total_mass*(part_gravity["head"]+part_gravity["neck"]+part_gravity["body"]+part_gravity["upper_arm"]+part_gravity["lower_arm"]+part_gravity["hand"]+part_gravity["upper_leg"]+part_gravity["lower_leg"]+part_gravity["foot"])
            return gravity_zone
        
        def get_trunk(np_pred_keypoints_3D):
            shoulder=np.nanmedian(np_pred_keypoints_3D[5:7,:],axis=0)
            base=np.nanmedian(np_pred_keypoints_3D[11:13,:],axis=0)
            trunk=np.nanmedian(np.vstack([shoulder,base]),axis=0)
            print(trunk)
            return trunk
        
        if self.model_type=="KP":
            np_pred_keypoints=detect_kp(rgb_array)
            if len(np_pred_keypoints)>1:
                np_pred_keypoints_3D=get_position_kp(rgb_array,dpt_array,np_pred_keypoints,proj_mtx)
                gravity_zone=get_gravity_zone(np_pred_keypoints_3D)
                trunk=get_trunk(np_pred_keypoints_3D)
                output_data=np.vstack([gravity_zone,trunk,np_pred_keypoints_3D]).flatten()
                output_data=np.insert(output_data,0,self.get_time())
                return output_data

    def write_log(self,output_data,csvpath):
        try:
            with open(csvpath, 'a') as f_handle:
                np.savetxt(f_handle,[output_data],delimiter=",")
        except FileNotFoundError:
            np.savetxt(self.logcsvpath,[output_data],delimiter=",")
        pass            

    def publish_tf(self,output_data):
        tf_kp_list=[]
        np_pred_keypoints_3D=output_data[1:].reshape(-1,4)
        for i,kp_3d in enumerate(np_pred_keypoints_3D):
            if i==0:
                tf_name=f"hmn"
            elif i==1:
                tf_name=f"hmn_trunk"
            else:
                tf_name=f"hmn_joint_{str(i).zfill(2)}"
            t = geometry_msgs.msg.TransformStamped()
            # t.header.frame_id = "zed_left"
            t.header.frame_id = "zed_left_camera_optical_frame_tate"
            t.header.stamp = rospy.Time.now()
            t.child_frame_id = tf_name
            if not np.isnan(kp_3d[0]):
                # t.transform.translation.x = gravity_zone[2]/1000
                # t.transform.translation.y = -gravity_zone[0]/1000
                # t.transform.translation.z = gravity_zone[1]/1000
                # if not np.isnan(gravity_zone[0]):
                t.transform.translation.x = kp_3d[0]
                t.transform.translation.y = kp_3d[1]
                t.transform.translation.z = kp_3d[2]
                t.transform.rotation.x = 0.0
                t.transform.rotation.y = 0.0
                t.transform.rotation.z = 0.0
                t.transform.rotation.w = 1.0
                tf_kp_list.append(t)
        tfm = tf2_msgs.msg.TFMessage(tf_kp_list)
        self.pub_tf.publish(tfm)
        rospy.loginfo("timestamp: "+str(time.time()))


    def ImageCallback(self,rgb_data,dpt_data,info_data):
        self.logger.debug("ImageCallback start")
        # extract image
        rgb_array=self.get_image(rgb_data,datatype="rgb_ZED")
        dpt_array=self.get_image(dpt_data,datatype="dpt")
        proj_mtx=np.array(info_data.P).reshape(3,4)

        # keypoint detection
        output_data=self.get_position(rgb_array,dpt_array,proj_mtx)
        self.logger.debug(output_data)
        # rospy.loginfo(output_data)

        try:
            # log (csv)
            self.write_log(output_data,csvpath=self.logcsvpath)
            # tf
            self.publish_tf(output_data)
            self.logger.info("processed successfully")
        except TypeError as e:# output_dataがない（get_positionがreturnされずNoneの場合）
            self.logger.warning(e)
            pass
        
detector=bdboxDetector()
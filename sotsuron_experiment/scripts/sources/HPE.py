#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
- カメラからImageがpublishされる
- ライブラリがsubscribeして、bboxとkeypointを検出して、それをpublish（またはreturn）する
- subscribe（またはreturn受け取り）して補償をかける
- bounding boxとkeypointが推定される
"""
import os
import cv2
import time
import numpy as np
import torch

import rospy
import message_filters
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo

from sotsuron_experiment.sotsuron_experiment.scripts.sources.detectron2_core import Detector




class HPE():
    def __init__(self,model="yolov5",model_type="KP",topicName_rgb=False,topicName_dpt=False,topicName_camInfo=False):
        self.model=model
        self.model_type=model_type
        self.topicName_rgb=topicName_rgb
        self.topicName_dpt=topicName_dpt
        self.topicName_camInfo=topicName_camInfo
        
        # modelの初期化
        if self.model=="yolov5":
            self.model = torch.hub.load("/usr/local/lib/python3.8/dist-packages/yolov5", 'custom', path=os.environ['HOME']+'/catkin_ws/src/object_detector/config/yolov5/yolov5s.pt',source='local')
            pass
        elif self.model=="yolov7":
            # kpができずに苦戦中。ODなら下の行で実行可
            # self.model = torch.hub.load(os.environ['HOME']+"/catkin_ws/src/object_detector/scripts/reference/yolov7", 'custom', source='local', path_or_model=os.environ['HOME']+'/catkin_ws/src/object_detector/scripts/reference/yolov7/yolov7.pt')
            # exec(open("reference/yolov7/kp_test.py").read())
            # subprocess.call("python3 reference/yolov7/kp_test.py",shell=True)
            
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            # print(os.getcwd())
            # os.chdir("reference/yolov7")
            # print(os.getcwd())

            self.model = torch.load('yolov7-w6-pose.pt', map_location=device)['model']

            pass
        elif self.model=="detectron2":
            self.model_OD=Detector(model_type="OD")
            self.model_IS=Detector(model_type="KP")
            pass
        elif self.model=="openpose":
            pass
        else:
            print("model not supported")
        
        # ImageのSubscriber定義
        rospy.init_node("HPE")
        mf=self.pub_sub()
        mf.registerCallback(self.ImageCallback)
        rospy.spin()

    
    def pub_sub(self):
        # subscriber
        sub_list=[]
        if self.topicName_rgb:
            sub_rgb=message_filters.Subscriber(self.topicName_rgb,Image)
            sub_list.append(sub_rgb)
        if self.topicName_dpt:
            sub_dpt=message_filters.Subscriber(self.topicName_dpt,Image)
            sub_list.append(sub_dpt)
        if self.topicName_camInfo:
            sub_camInfo=message_filters.Subscriber(self.topicName_camInfo,CameraInfo)
            sub_list.append(sub_camInfo)
        mf=message_filters.ApproximateTimeSynchronizer(sub_list,100,5)

        return mf
        # ImageCallback: modelに画像を投げる

    def ImageCallback(self,topic_rgb,topic_dpt="False",topic_camInfo="False"):
        if self.model=="yolov5":
            pass
        elif self.model=="yolov7":
            pass
        elif self.model=="detectron2":
            # Object Detection (bounding box)
            if topic_rgb:
                try:
                    bridge = CvBridge()
                    rgb_array = bridge.imgmsg_to_cv2(topic_rgb)
                    rgb_array=cv2.cvtColor(rgb_array,cv2.COLOR_BGR2RGB)
                    # plt.imshow(rgb_array)
                    # plt.pause(.001)
                    # cv2.imshow("rgb",rgb_array)
                    # cv2.imwrite("/home/hayashide/catkin_ws/src/object_detector/scripts/monitor/rgb.jpg",rgb_array)
                    print("rgb show")

                except Exception as err:
                    rospy.logerr(err)
            if topic_dpt:
                dpt_array = np.frombuffer(topic_dpt.data, dtype=np.uint16).reshape(topic_dpt.height, topic_dpt.width, -1)
                dpt_array=np.nan_to_num(dpt_array)
                dpt_array_show=(dpt_array-np.min(dpt_array))/(np.max(dpt_array)-np.min(dpt_array))*255
                dpt_array_show=cv2.applyColorMap(np.uint8(dpt_array_show),cv2.COLORMAP_JET)
                # cv2.imwrite("/home/hayashide/catkin_ws/src/object_detector/scripts/monitor/depth.jpg",dpt_array_show)
                cv2.imshow("depth",dpt_array_show)
                print("dpt show")
                pass
            if topic_camInfo:
                pass
            cv2.waitKey(1)
            
            bbox_list=list(self.model_OD.onImage(image_mat=rgb_array))
            print(bbox_list)
            # KeyPoint Detection (姿勢推定)
            pass
        elif self.model=="openpose":
            pass
        else:
            print("model not supported")
        pass


# topicName_rgb="/camera5/camera/color/image_raw"
# topicName_dpt="/camera5/camera/aligned_depth_to_color/image_raw"
# topicName_camInfo="/camera5/camera/aligned_depth_to_color/camera_info"

topicName_rgb="/camera3/camera/color/image_raw"
topicName_dpt="/camera3/camera/aligned_depth_to_color/image_raw"
topicName_camInfo="/camera3/camera/aligned_depth_to_color/camera_info"
# hpe=HPE(model="detectron2",model_type="None",topicName_rgb=topicName_rgb,topicName_dpt=topicName_dpt,topicName_camInfo=topicName_camInfo)
hpe=HPE(model="yolov5",model_type="None",topicName_rgb=topicName_rgb,topicName_dpt=topicName_dpt,topicName_camInfo=topicName_camInfo)



"""
all topics published by realsense
/camera5/camera/align_to_color/parameter_descriptions
/camera5/camera/align_to_color/parameter_updates
/camera5/camera/aligned_depth_to_color/camera_info
/camera5/camera/aligned_depth_to_color/image_raw
/camera5/camera/aligned_depth_to_color/image_raw/compressed
/camera5/camera/aligned_depth_to_color/image_raw/compressed/parameter_descriptions
/camera5/camera/aligned_depth_to_color/image_raw/compressed/parameter_updates
/camera5/camera/aligned_depth_to_color/image_raw/compressedDepth
/camera5/camera/aligned_depth_to_color/image_raw/compressedDepth/parameter_descriptions
/camera5/camera/aligned_depth_to_color/image_raw/compressedDepth/parameter_updates
/camera5/camera/aligned_depth_to_color/image_raw/theora
/camera5/camera/aligned_depth_to_color/image_raw/theora/parameter_descriptions
/camera5/camera/aligned_depth_to_color/image_raw/theora/parameter_updates
/camera5/camera/color/camera_info
/camera5/camera/color/image_raw
/camera5/camera/color/image_raw/compressed
/camera5/camera/color/image_raw/compressed/parameter_descriptions
/camera5/camera/color/image_raw/compressed/parameter_updates
/camera5/camera/color/image_raw/compressedDepth
/camera5/camera/color/image_raw/compressedDepth/parameter_descriptions
/camera5/camera/color/image_raw/compressedDepth/parameter_updates
/camera5/camera/color/image_raw/theora
/camera5/camera/color/image_raw/theora/parameter_descriptions
/camera5/camera/color/image_raw/theora/parameter_updates
/camera5/camera/color/metadata
/camera5/camera/depth/camera_info
/camera5/camera/depth/color/points
/camera5/camera/depth/image_rect_raw
/camera5/camera/depth/image_rect_raw/compressed
/camera5/camera/depth/image_rect_raw/compressed/parameter_descriptions
/camera5/camera/depth/image_rect_raw/compressed/parameter_updates
/camera5/camera/depth/image_rect_raw/compressedDepth
/camera5/camera/depth/image_rect_raw/compressedDepth/parameter_descriptions
/camera5/camera/depth/image_rect_raw/compressedDepth/parameter_updates
/camera5/camera/depth/image_rect_raw/theora
/camera5/camera/depth/image_rect_raw/theora/parameter_descriptions
/camera5/camera/depth/image_rect_raw/theora/parameter_updates
/camera5/camera/depth/metadata
/camera5/camera/extrinsics/depth_to_color
/camera5/camera/motion_module/parameter_descriptions
/camera5/camera/motion_module/parameter_updates
/camera5/camera/pointcloud/parameter_descriptions
/camera5/camera/pointcloud/parameter_updates
/camera5/camera/realsense2_camera_manager/bond
/camera5/camera/rgb_camera/auto_exposure_roi/parameter_descriptions
/camera5/camera/rgb_camera/auto_exposure_roi/parameter_updates
/camera5/camera/rgb_camera/parameter_descriptions
/camera5/camera/rgb_camera/parameter_updates
/camera5/camera/stereo_module/auto_exposure_roi/parameter_descriptions
/camera5/camera/stereo_module/auto_exposure_roi/parameter_updates
/camera5/camera/stereo_module/parameter_descriptions
/camera5/camera/stereo_module/parameter_updates

"""
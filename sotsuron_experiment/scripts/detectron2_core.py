from importlib.metadata import metadata
import time
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo

import cv2
import numpy as np
import torch
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class Detector:
    def __init__(self,model_type="OD"):
        self.cfg=get_cfg()
        self.model_type=model_type

        # Load model config and pretrained model
        if model_type=="OD": # Object Detection
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS=model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
        elif model_type=="IS": # Instance Segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS=model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        elif model_type=="LVIS": # LVInstance Segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file("LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml"))
            self.cfg.MODEL.WEIGHTS=model_zoo.get_checkpoint_url("LVISv0.5-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_1x.yaml")
        elif model_type=="PS": # Panoptic Segmentation
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml"))
            self.cfg.MODEL.WEIGHTS=model_zoo.get_checkpoint_url("COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml")
        elif model_type=="KP": # KeyPoint detection
            self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
            self.cfg.MODEL.WEIGHTS=model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST=0.7
        self.cfg.MODEL_DEVICE="cuda"

        self.predictor=DefaultPredictor(self.cfg)
    
    def onImage(self, imagePath=False, image_mat=False, savePath="/home/hayashide/catkin_ws/src/object_detector/images/save.jpg"):
        if image_mat.any():
            image=image_mat
        if imagePath:
            image=cv2.imread(imagePath)
        image=cv2.resize(image,(640,480))
        torch.cuda.empty_cache()
        if self.model_type != "PS":
            predictions=self.predictor(image)

            viz=Visualizer(image[:,:,::-1],
            metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
            instance_mode=ColorMode.IMAGE_BW)

            # print(predictions['instances'].pred_keypoints)


            output=viz.draw_instance_predictions(predictions["instances"].to("cpu"))
        else:
            predictions,segmentInfo=self.predictor(image)["panoptic_seg"]
            viz=Visualizer(image[:,:,::-1],
            MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
            output=viz.draw_panoptic_seg_predictions(predictions.to("cpu"),segmentInfo)
        
        cv2.imwrite(savePath,output.get_image()[:,:,::-1])
        if self.model_type=="OD":
            print(predictions["instances"])
            """
            {
                'instances': Instances(num_instances=2, image_height=480, image_width=640, fields=[pred_boxes: Boxes(tensor([[2.9253e+02, 0.0000e+00, 6.3970e+02, 4.7950e+02],
        [3.1455e-01, 4.2435e+02, 1.4486e+02, 4.7753e+02]], device='cuda:0')), 
                scores: tensor([0.9987, 0.7032], device='cuda:0'), 
                pred_classes: tensor([0, 0], device='cuda:0')])}
            """
            return predictions['instances'].pred_boxes.to(torch.device('cpu'))
        if self.model_type=="KP":
            return predictions['instances'].pred_keypoints
        print("##### DEBUG NOW #####")
        cv2.imshow("Result",output.get_image()[:,:,::-1])
        # cv2.waitKey(1)

        key=cv2.waitKey(1) & 0xFF
        if key ==ord("q"):
            cv2.destroyallwindows()

    def onVideo(self,videoPath,savePath=False,csvPath=False):
        cap=cv2.VideoCapture(videoPath)

        (success,image)=cap.read()
        
        size=image.shape[1],image.shape[0]
        
        if savePath:
            fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
            video=cv2.VideoWriter(savePath,fourcc, 7.0,size)

        if (cap.isOpened()==False):
            print("Error in opening the file...")
            return
        

        history=[]
        i=0

        while success:
            image=cv2.resize(image,size)
            if self.model_type != "PS":
                predictions=self.predictor(image)

                viz=Visualizer(image[:,:,::-1],
                metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
                instance_mode=ColorMode.IMAGE_BW)

                output=viz.draw_instance_predictions(predictions["instances"].to("cpu"))
            else:
                predictions,segmentInfo=self.predictor(image)["panoptic_seg"]
                viz=Visualizer(image[:,:,::-1],
                MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
                output=viz.draw_panoptic_seg_predictions(predictions.to("cpu"),segmentInfo)
            
            if csvPath:
                pred_keypoints=predictions['instances'].pred_keypoints
                try:
                    np_pred_keypoints=pred_keypoints.to(torch.device('cpu')).detach().clone().numpy()[0]
                    np_pred_keypoints_time=np.insert(np_pred_keypoints,0,i)
                    history.append(np_pred_keypoints_time)
                except IndexError:
                    try:
                        np_pred_keypoints=np.full_like(np_pred_keypoints,np.nan)
                    except UnboundLocalError:
                        np_pred_keypoints=np.full((1,51),np.nan)
                    np_pred_keypoints_time=np.insert(np_pred_keypoints,0,i)
                    history.append(np_pred_keypoints_time)
                np.savetxt(csvPath,history,delimiter=",")


            cv2.imshow("Result",output.get_image()[:,:,::-1])
            if savePath:
                video.write(output.get_image()[:,:,::-1])
                print("filename:",savePath,"add frame:",time.time())
            key=cv2.waitKey(1) & 0xFF
            if key ==ord("q"):
                break
        
            (success,image)=cap.read()

            i+=1/30

        if savePath:
            video.release()
            print("video released")

    def onLive(self):
        cap=cv2.VideoCapture(0)

        if (cap.isOpened()==False):
            print("Error in opening the file...")
            return
        
        (success,image)=cap.read()

        while success:
            image=cv2.resize(image,(1080,720))
            if self.model_type != "PS":
                predictions=self.predictor(image)

                viz=Visualizer(image[:,:,::-1],
                metadata=MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
                instance_mode=ColorMode.IMAGE_BW)

                output=viz.draw_instance_predictions(predictions["instances"].to("cpu"))
            else:
                predictions,segmentInfo=self.predictor(image)["panoptic_seg"]
                viz=Visualizer(image[:,:,::-1],
                MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]))
                output=viz.draw_panoptic_seg_predictions(predictions.to("cpu"),segmentInfo)

            cv2.imshow("Result",output.get_image()[:,:,::-1])
            key=cv2.waitKey(1) & 0xFF
            if key ==ord("q"):
                break
        
            (success,image)=cap.read()

    def onROS(self,topicName='/hsrb/head_rgbd_sensor/rgb/image_rect_color'):
        rospy.init_node('detectron2')
        spin_rate=rospy.Rate(30)
        bridge=CvBridge()
        input_image=None

        def color_image_cb(data):
            try:
                global input_image
                input_image = bridge.imgmsg_to_cv2(data, "bgr8")
                print("here")
                spin_rate.sleep()
            except CvBridgeError as cv_bridge_exception:
                rospy.logerr(cv_bridge_exception)



        # Subscribe color image data from HSR
        # Wait until connection
        # rospy.wait_for_message(topicName, Image, timeout=5.0)
        image_sub = rospy.Subscriber(topicName, Image, color_image_cb)
        while not rospy.is_shutdown():
            time.sleep(0.01)
            try:
                cv2.imshow("HSR eye",input_image)
                cv2.waitKey(3)
            except cv2.error as e:
                print(e)
                pass
        cv2.destroyAllWindows()
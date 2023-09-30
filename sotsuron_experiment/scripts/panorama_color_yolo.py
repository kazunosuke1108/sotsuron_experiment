#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
import shutil
import cv2
import torch
import numpy as np
from glob import glob
import scipy.optimize as op
import matplotlib.pyplot as plt
from detectron2_core import *

# yolov5 model import
model = torch.hub.load("/usr/local/lib/python3.8/dist-packages/yolov5", 'custom', path=os.environ['HOME']+'/catkin_ws/src/object_detector/config/yolov5/yolov5s.pt',source='local')
detector=Detector(model_type="KP")


def save_frame_range_sec(video_path, start_sec, stop_sec, step_sec,
                         dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    fps = cap.get(cv2.CAP_PROP_FPS)
    fps_inv = 1 / fps

    sec = start_sec
    while sec < stop_sec:
        n = round(fps * sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(
                '{}_{}_{:.2f}.{}'.format(
                    base_path, str(n).zfill(digit), n * fps_inv, ext
                ),
                frame
            )
        else:
            return
        sec += step_sec



def match_feature(img1, img2):
    # SIFTを用意
    sift = cv2.SIFT_create()
    # 特徴点とdescriberを検出
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    # マッチさせる
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []  # オブジェクトの保管場所
    good2 = []  # オブジェクトの保管場所 drawMatchesKnnに食わせるための形式
    for m, n in matches:
        if m.distance < 0.5*n.distance:  # 厳選を実施
            good.append(m)
            good2.append([m])
    img1_pt = [list(map(int, kp1[m.queryIdx].pt))
               for m in good]  # マッチした１枚目の特徴点
    img2_pt = [list(map(int, kp2[m.trainIdx].pt))
               for m in good]  # マッチした２枚目の特徴点
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good2,
                             None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)  # マッチ状況の描画
    # plt.imshow(img3), plt.show()  # 確認のためマッチの様子を出力

    img1_pt_s = []  # 重複削除後のマッチした特徴点
    img2_pt_s = []
    for i in range(len(img1_pt)):
        if (img1_pt[i] not in img1_pt_s) and (img2_pt[i] not in img2_pt_s):  # 重複の確認
            img1_pt_s.append(img1_pt[i])
            img2_pt_s.append(img2_pt[i])

    img1_pt_s = np.array(img1_pt_s)  # 最適化に備えnumpy形式に変換
    img2_pt_s = np.array(img2_pt_s)
    return img1_pt_s, img2_pt_s

def error_func(t):
    # 特徴点の合致における誤差関数
    answer = 0
    for i in range(len(img1_pt_s)):  # 特徴点の組毎に足しこむ
        # 特徴点間の距離の2乗
        answer += (np.linalg.norm(t+img2_pt_s[i]-img1_pt_s[i]))**2
    t_x.append(t[0])  # プロットのための記録
    t_y.append(t[1])
    accum.append(answer)
    return answer

movie_dir="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0117/movie"
frames_dir="/home/hayashide/catkin_ws/src/sotsuron_experiment/heavy/frames"
results_dir="/home/hayashide/catkin_ws/src/sotsuron_experiment/results/0117/results/panorama"

movie_paths=sorted(glob(movie_dir+"/*.mp4"))
print(movie_paths)

for i, movie_path in enumerate(movie_paths):

    basename=os.path.basename(movie_path)
    if os.path.isdir(frames_dir+"/"+basename[:-4]):
        shutil.rmtree(frames_dir+"/"+basename[:-4])
    os.makedirs(frames_dir+"/"+basename[:-4],exist_ok=True)
    # os.makedirs(results_dir+"/"+basename[:-4],exist_ok=True)
    imgs=[]
    imgs_color=[]


    save_frame_range_sec(movie_path,
                        10, 35, 0.225,
                        frames_dir+"/"+basename[:-4], basename[:-4])

    img_paths=sorted(glob(frames_dir+"/"+basename[:-4]+"/*"))
    for img_path in img_paths:
        temp_img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
        imgs.append(temp_img)
        temp_img=cv2.imread(img_path)
        imgs_color.append(temp_img)

    # 結果出力のキャンバスを作成
    canvas_h, canvas_w = 2000, 3000
    canvas = np.zeros((canvas_h, canvas_w,3))
    canvas += 255
    height, width = imgs[0].shape

    # 1枚目の写真を貼る
    if "_23_" in movie_path or "_24_" in movie_path:
        vector_root=np.array([500,1500])
    else:
        vector_root = np.array([500, 100])
    # canvas[int(vector_root[0]):int(vector_root[0])+height,
    #     int(vector_root[1]):int(vector_root[1])+width,:] = imgs_color[0]

    for i in range(len(imgs)-2):#range(len(imgs)-2,1,-1):
        # 写真の名前を定義
        img1 = imgs[i]
        img2 = imgs[i+1]
        img1_color = imgs_color[i]
        img2_color = imgs_color[i+1]
        # マッチする特徴点を抽出
        try:
            img1_pt_s, img2_pt_s = match_feature(img1, img2)
        except:
            continue
        # 最適化可視化のための記録リスト
        t_x = []
        t_y = []
        accum = []
        # 最適なベクトルtの探索
        vec = op.minimize(error_func, [0, 500]).x
        # 前回のベクトルに足し込むことで全体座標系での移動量を求める
        vector = np.array([vec[1], vec[0]])+vector_root
        print(vector)
        if "_23_" in movie_path or "_24_" in movie_path:
            if i!=0:
                if vector[1]>=vector_old[1]:
                    vector_old=vector
                    continue
                else:
                    vector_old=vector
            else:
                vector_old=vector

        else:
            if i!=0:
                if vector[1]<=vector_old[1]:
                    vector_old=vector
                    continue
                else:
                    vector_old=vector
            else:
                vector_old=vector

        # これから貼り付ける画像の大きさを取得
        height, width = img2.shape
        # 現状の値と貼り付け画像の平均をとって貼り付ける
        # print(vector)
        # print(img2.shape)

        # 人のいる場所を切り出す
        try:
            results=model(img2_color)
            objects=results.pandas().xyxy[0]
            obj_people=objects[objects['name']=='person']
            # print(obj_people)
            trim=[int(obj_people['xmin'][0]-5),int(obj_people['xmax'][0]+5)]
        except Exception:
            continue
            # trim=[500,800]

        # if i<(len(imgs)-2)/2+6:
        #     trim=[500,800]
        # else:
        #     trim=[600,900]
        # trim=[0,1280]
        # koyui=img2_color<0
        # # print(koyui)
        # img2_color=img2_color*(1-koyui)+200*koyui
        # try:
        [pred_keypoints,img2_color]=detector.onImage(image_mat=img2_color,return_skeleton=True)
        # except RuntimeError:
        #     pass
        try:
            canvas[int(vector[0]):int(vector[0])+height, int(vector[1])+trim[0]:int(vector[1])+trim[1],:] = (img2_color[:,trim[0]:trim[1],:] +
                                                                                            canvas[int(vector[0]):int(vector[0])+height, int(vector[1])+trim[0]:int(vector[1])+trim[1],:])/2
        except ValueError:
            pass
        # canvas[int(vector[0]):int(vector[0])+height, int(vector[1]):int(vector[1])+width] = (img2 +
        #                                                                                      canvas[int(vector[0]):int(vector[0])+height, int(vector[1]):int(vector[1])+width])/2

        vector_root = vector
        # 最適化過程のプロット
        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        # ax.plot(t_x, t_y, accum)
        # plt.show()
        cv2.imwrite(results_dir+"/"+basename[:-4]+"0225.jpg", canvas)
        
    # 完成した画像を保存
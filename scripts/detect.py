#!/usr/bin/python
# -*- coding: utf-8 -*-

# import general utilities
import os
from PIL import Image
import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

# import some common detectron2 utilities
import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

# setup detectron2 logger
from detectron2.utils.logger import setup_logger
setup_logger()

# setup detection model
def setup_detection_model(treshold):
    cfg = get_cfg()
    cfg.MODEL.DEVICE = 'cpu'
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = treshold  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)

    return predictor


def crop_faces(out):

    found_faces = []

    n = len(out["instances"])
    # print(n)
    localout = out["instances"].to("cpu")
    # print(localout)

    boxes = localout.pred_boxes.tensor.numpy()
    # print(boxes)
    keypoints = localout.pred_keypoints.numpy()

    # height, width = shape[0:2] was used to crop out faces relative to height and size of the image. now replaced by size of the detectron boxes
    #marge_x = width * 0.01
    #marge_y = 0

    # ander idee voor marge: afstand tussen de twee punten van de boxes gebruiken 
    for i in range(0, n):

        x1, y1, x2, y2 = boxes[i]  # bounding box of person

        marge_x = (x2 - x1) * 0.05 
        marge_y = (y2 - y1) * 0.15

        x_nose, y_nose, s_nose = keypoints[i][0]  # nose keypoint
        x_l_ear, y_l_ear, s_l_ear = keypoints[i][3]  # left_ear keypoint
        x_r_ear, y_r_ear, s_r_ear = keypoints[i][4]  # right_ear keypoint
        # left_shoulder keypoint
        x_l_shoulder, y_l_shoulder, s_l_shoulder = keypoints[i][5]
        # right_schoulder keypoint
        x_r_shoulder, y_r_shoulder, s_r_shoulder = keypoints[i][6]

        # Determine X-values
        if x_r_ear <= x_nose <= x_l_ear:  # nose between ears is front profile of face
            if x_r_ear - marge_x > 0:
                x1 = x_r_ear - marge_x
            else:
                x1 = x_r_ear
            if x_l_ear + marge_x < x2:
                x2 = x_l_ear + marge_x
            else:
                x2 = x_l_ear

        elif x_r_ear < x_nose:  # side profil (looking to the right)
            if x_r_ear - marge_x > 0:
                x1 = x_r_ear - marge_x
            else:
                x1 = x_r_ear
            if x_nose + marge_x < x2:
                x2 = x_nose + marge_x
            else:
                x2 = x_nose

        elif x_nose < x_r_ear:  # side profil (looking to the left)
            if x_nose - marge_x > 0:
                x1 = x_nose - marge_x
            else:
                x1 = x_nose
            if x_r_ear + marge_x < x2:
                x2 = x_r_ear + marge_x
            else:
                x2 = x_r_ear

        # Determine bottom Y-value
        if s_l_shoulder > 0.05 and s_r_shoulder > 0.05:
            if y_l_shoulder > y_r_shoulder:
                if y_r_shoulder + marge_y < y2:
                    y2 = y_r_shoulder
                else:
                    y2 = y_r_shoulder - marge_y
            else:
                if y_l_shoulder + marge_y < y2:
                    y2 = y_l_shoulder
                else:
                    y2 = y_l_shoulder - marge_y

        #cropped_image = image[int(y1):int(y2), int(x1):int(x2)]
        found_faces.append((int(y1), int(x2), int(y2), int(x1)))

        # opencvImage = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
        # plt.imshow(opencvImage)
        # plt.show()
    print("[INFO] " + str(len(found_faces)) + " faces found")
    return found_faces


def create_list_images(csv_file):
    print("[INFO] creating a list of image paths")
    d = {}
    paths = pd.read_csv(csv_file).values.tolist()
    for path in paths:
        d[path[0]] = path[1]

    print("[INFO] Count of images: " + str(len(paths)))
    # for p in all_faces:
    # print(p)
    return d


def detecting_faces(csv_file, predictor):
    i = 1
    index_face = 1

    # loop over the image paths
    all_paths = create_list_images(csv_file)
    for image_path in all_paths.keys():
        # load the input image and convert it from RGB (OpenCV ordering) to dlib ordering (RGB)
        print(i, "[INFO] processing image {}".format(image_path))

        # Use detectron for face detection
        try:
            image = cv2.imread(image_path)
            # Inference with a keypoint detection model
            # shape = image.shape
            out = predictor(image)
            faces = crop_faces(out)
            # print(faces)

            for face in faces:
                print("[INFO] processing face nr. " + str(index_face))
                (top, right, bottom, left) = face
                cropped_image = image[top:bottom, left:right]
                #filepath = os.path.join("data/faces", str(index_face) + ".png")
                #save_image(cropped_image, filepath)
                # plt.imshow(cropped_image)
                # plt.show()
                results = [image_path,all_paths[image_path], face]
                write_csv(results)
                index_face = index_face+1
        except:
            print("[ERROR] could not open image {}".format(image_path))

        i = i+1

    print("[INFO] Total faces found: " + str(index_face))
    print("Faces found and saved to drive")

# Save faces as seperate images
def save_image(image, filepath):
    try:
        opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        PIL_image = Image.fromarray(opencvImage)
        #plt.imsave(filepath, opencvImage)
        PIL_image.thumbnail((256,256))
        PIL_image.save(filepath)
    except:
        print("[ERROR] could not save cropped image {}".format(filepath))

# Save information in CSV
def write_csv(line):
    with open("data/found-faces.csv", 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(line)
    csv_file.close()

def detect_and_crop(csv_file, treshold):
    print("[INFO] Step 1: start detecting faces")
    csv_header = ['image_path', 'name', 'face_location']
    with open("data/found-faces.csv", 'w') as result_file:
        writer = csv.writer(result_file)
        writer.writerow(csv_header)
    result_file.close()
    predictor = setup_detection_model(treshold)
    detecting_faces(csv_file, predictor)
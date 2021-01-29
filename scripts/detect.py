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
# needs an image
def setup_detection_model(image, treshold):
    cfg = get_cfg()
    cfg.MODEL.DEVICE = 'cpu'
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = treshold  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)

    # Inference with a keypoint detection model
    outputs = predictor(image)

    # v = Visualizer(
    #    im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    #out = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    # opencvImage = cv2.cvtColor(out.get_image()[:, :, ::-1], cv2.COLOR_RGB2BGR)
    # plt.imshow(opencvImage)
    # plt.show()

    return outputs


def crop_face(image, out):

    found_faces = []

    n = len(out["instances"])
    # print(n)
    localout = out["instances"].to("cpu")
    # print(localout)

    boxes = localout.pred_boxes.tensor.numpy()
    # print(boxes)
    keypoints = localout.pred_keypoints.numpy()

    marge = 100
    for i in range(0, n):

        x1, y1, x2, y2 = boxes[i]  # bounding box of person

        x_nose, y_nose, s_nose = keypoints[i][0]  # nose keypoint
        x_l_ear, y_l_ear, s_l_ear = keypoints[i][3]  # left_ear keypoint
        x_r_ear, y_r_ear, s_r_ear = keypoints[i][4]  # right_ear keypoint
        # left_shoulder keypoint
        x_l_shoulder, y_l_shoulder, s_l_shoulder = keypoints[i][5]
        # right_schoulder keypoint
        x_r_shoulder, y_r_shoulder, s_r_shoulder = keypoints[i][6]

        # Determine X-values
        if x_r_ear <= x_nose <= x_l_ear:  # nose between ears is front profile of face
            if x_r_ear - marge > 0:
                x1 = x_r_ear - marge
            else:
                x1 = x_r_ear
            if x_l_ear + marge < x2:
                x2 = x_l_ear + marge
            else:
                x2 = x_l_ear

        elif x_r_ear < x_nose:  # side profil (looking to the right)
            if x_r_ear - marge > 0:
                x1 = x_r_ear - marge
            else:
                x1 = x_r_ear
            if x_nose + marge < x2:
                x2 = x_nose + marge
            else:
                x2 = x_nose

        elif x_nose < x_r_ear:  # side profil (looking to the left)
            if x_nose - marge > 0:
                x1 = x_nose - marge
            else:
                x1 = x_nose
            if x_r_ear + marge < x2:
                x2 = x_r_ear + marge
            else:
                x2 = x_r_ear

        # Determine bottom Y-value
        if s_l_shoulder > 0.05 and s_r_shoulder > 0.05:
            if y_l_shoulder > y_r_shoulder:
                if y_r_shoulder + marge < y2:
                    y2 = y_r_shoulder + marge
                else:
                    y2 = y_r_shoulder
            else:
                if y_l_shoulder + marge < y2:
                    y2 = y_l_shoulder + marge
                else:
                    y2 = y_l_shoulder

        cropped_image = image[int(y1):int(y2), int(x1):int(x2)]
        found_faces.append((int(y1), int(x2), int(y2), int(x1)))

        # opencvImage = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
        # plt.imshow(opencvImage)
        # plt.show()
    print("[INFO] " + str(len(found_faces)) + " faces found")
    return found_faces


# Create a list with all images (combine images with portraits)

def create_list_images(csv_file):
    print("[INFO] creating a list of image paths")
    # all_faces.clear()
    d = {}
    paths = pd.read_csv(csv_file).values.tolist()
    for path in paths:
        d[path[0]] = path[1]

    print("[INFO] Count of images: " + str(len(paths)))
    # for p in all_faces:
    # print(p)
    return d


def detecting_faces(csv_file, treshold):
    i = 1
    index_face = 1
    found_faces_info = [['image_path', 'name', 'face_location', 'crop']]

    # loop over the image paths
    all_paths = create_list_images(csv_file)
    for image_path in all_paths.keys():
        # load the input image and convert it from RGB (OpenCV ordering) to dlib ordering (RGB)
        print(i, "[INFO] processing image {}".format(image_path))

        # Use detectron for face detection
        image = cv2.imread(image_path)
        out = setup_detection_model(image, treshold)
        faces = crop_face(image, out)
        # print(faces)

        for face in faces:
            print("[INFO] processing face nr. " + str(index_face))
            (top, right, bottom, left) = face
            cropped_image = image[top:bottom, left:right]
            filepath = os.path.join("data/faces", str(index_face) + ".png")
            save_image(cropped_image, filepath)
            # plt.imshow(cropped_image)
            # plt.show()
            results = [image_path,all_paths[image_path], face, filepath]
            found_faces_info.append(results)
            index_face = index_face+1

        i = i+1

    print("[INFO] Total faces found: " + str(len(found_faces_info)-1))
    write_csv(found_faces_info)
    print("Faces found and saved to drive")

# Save faces as seperate images
def save_image(image, filepath):
    opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    plt.imsave(filepath, opencvImage)
    return filepath

# Save information in CSV
def write_csv(lines):
    with open("data/found-faces.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(lines)
    csv_file.close()

def detect_and_crop(csv_file, treshold):
    print("[INFO] Step 1: start detecting faces")
    detecting_faces(csv_file, treshold)
#!/usr/bin/python
# -*- coding: utf-8 -*-

# import some common detectron2 utilities
import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
import cv2
import pandas as pd
from pyfacy import utils
import numpy
import os
import csv

# workflow
# 1 de lijst met bestandsnamen (csv) wordt uitgelezen
# 2 op de foto wordt gekeken of er 1 of meer mensen op de foto staan
# 3 van deze gezichten wordt een encodering gemaakt
# 4 dit wordt weggeschreven in een CSV

treshold = 0.7
input_file = "filenames.csv"

def setup_detection_model(treshold):
    print("[INFO] setting up model...")
    cfg = get_cfg()
    cfg.MODEL.DEVICE = 'cpu'
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = treshold  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)

    return predictor

def get_faces(image):
    print("[INFO] finding faces...")
    found_faces = []
    outputs = predictor(image)
    instances = outputs["instances"]
    local_instances = instances.to("cpu")
    boxes = local_instances.pred_boxes.tensor.numpy()

    for i in range(0, len(instances)):
        x1, y1, x2, y2 = boxes[i]
        found_faces.append((int(y1), int(x2), int(y2), int(x1)))

    return found_faces

def encode_face(face):
    print("[INFO] encoding...")
    encoding = utils.img_to_encodings(face)
    if len(encoding) > 0:
        return "bruikbaar"
    return ''

def write_csv(lines):
    with open("preparation/kwaliteit.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(lines)
    csv_file.close()

def is_usable(faces, image):
    print("[INFO] encoding...")
    for face in faces:
            (top, right, bottom, left) = face
            encoding = utils.img_to_encodings(image[top:bottom, left:right])
            if len(encoding) > 0:
                return True
    return False

def create_folders():
    if not os.path.exists("preparation"):
        os.makedirs("preparation")

create_folders()
predictor = setup_detection_model(treshold)
list_photos = pd.read_csv(input_file).values.tolist()
results = [["path","bruikbaar?"]]
i = 0
usable_count = 0
for photo in list_photos:
    photo = photo[0]
    i = i+1
    print("[INFO] #{} - busy with {}".format(i, photo))
    image = cv2.imread(photo)
    faces = get_faces(image)
    if len(faces) > 0:
        if is_usable(faces, image):
            results.append([photo, 'bruikbaar'])
            usable_count = usable_count + 1
        else:
            results.append([photo, ''])
    else:
        results.append([photo, ''])
write_csv(results)
print("{} photos of the {} are usable".format(usable_count, len(list_photos)))
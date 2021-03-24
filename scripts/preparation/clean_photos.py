#!/usr/bin/python
# -*- coding: utf-8 -*-

# import some common detectron2 utilities
import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import cv2
import pandas as pd
import os
import csv



# workflow
# 1 de lijst met bestandsnamen (csv) wordt uitgelezen
# 2 op de foto wordt gekeken of er 1 of meer mensen op de foto staan
# 3 indien 1, dan zetten we deze op een CSV met portretten
#   indien 0, dan verwijderen we de foto van de lijst
#   indien meerdere, dan zetten we deze op een CSV met producties
# 4 als controle maken we ook een visualizer foto

cfg = get_cfg()
treshold = 0.7


# lines bestaat uit: index nr, filename, aantal gezichten
lines = [["index", "original", "aantal gezichten"]]

if not os.path.exists("data/test"):
    os.makedirs("data/test/portrets")
    os.mkdir("data/test/empty")
    os.mkdir("data/test/group")


# setup detection model
def setup_detection_model(treshold): 
    print("setting up model")  
    cfg.MODEL.DEVICE = 'cpu'
    cfg.merge_from_file(model_zoo.get_config_file(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = treshold  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    print("done with setting up model")
    return predictor

def write_data(data):
    print("writing data")
    with open("data/cleanup_portrets.csv", "w") as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerows(data)
    output_csv.close()
   

def is_portret(predictor, index, photo):
    print("is {} a portret?".format(photo))
    image = cv2.imread(photo)
    outputs = predictor(image)
    instances = outputs["instances"]
    count_instances = len(instances)

    lines.append([index, photo, count_instances])

    v = Visualizer(image, MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.0)
    v = v.draw_instance_predictions(instances.to("cpu"))
    
    if  count_instances == 1:
        print("one instance found on " + str(photo))
        cv2.imwrite("data/test/portrets/" + str(index) + ".jpg", v.get_image())
        return True

    elif count_instances == 0:
        print("zero instances found on " + str(photo))
        cv2.imwrite("data/test/empty/" + str(index) + ".jpg", v.get_image())
        return False

    print("multiple instances found on " + str(photo))
    cv2.imwrite("data/test/group/" + str(index) + ".jpg", v.get_image())
    return False

predictor = setup_detection_model(treshold)
list_photos = pd.read_csv("portrets.csv").values.tolist()
for index, photo in enumerate(list_photos):
    filename = photo[0].split("/")[-1]
    if is_portret(predictor, index, photo[0]):
        print("{} is a portret".format(filename))
    else:
        print("{} is not a portret".format(filename))

write_data(lines)

from sys import argv, path
import cv2
from helpers_detection_model import create_predictions, get_instances, setup_detection_model
import pandas as pd


treshold = 0.7
files = argv[1] # csv containing filenames

def create_prediction_image(photo):
    filename = photo.split("/")[-1]
    image = cv2.imread(photo)
    instances = get_instances(treshold, image)
    prediction_image = create_predictions(instances, image)
    cv2.imwrite(filename, prediction_image)


list_photos = pd.read_csv(files).values.tolist()
print(list_photos)
for photo in list_photos:
    print(photo)
    create_prediction_image(photo[0])

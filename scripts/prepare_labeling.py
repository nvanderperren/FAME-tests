import pickle
import csv
import pandas as pd
from math import isnan
import os

input_file = "/Users/nastasia/Downloads/face-clustering-results.pickle"
descriptive_metadata = "data/kunstenpunt_data.csv"

def create_list_metadata(csv_file):
    print("[INFO] creating a list of metadata items")
    d = {}
    paths = pd.read_csv(csv_file).values.tolist()
    for path in paths:
        QID = path[6]
        if not str(QID) == 'nan':
            QID = 'https://www.wikidata.org/wiki/' + str(QID)
        d[path[0]] = [path[1], path[2], path[3], QID]

    print("[INFO] Count of items: " + str(len(paths)))
    # for p in all_faces:
    # print(p)
    return d

def combine_data(paths, list_metadata):
    print("[INFO] combining metadata and face")
    metadata = []
    for path in paths:
        if path in list_metadata.keys():
            metadata.append(list_metadata[path])
        else:
            metadata.append(['', '', '', ''])
    print("[INFO] Count of faces: " + str(len(metadata)))
    data = pd.DataFrame(metadata, columns=["gezelschap", "productie", "seizoen", "wikidata"])
    data.to_csv("data/labeling/metadata.csv", index=True, index_label="ID")

def create_labeling_images(data):
    labeling = data[['name', 'crop', 'neighbors', 'prediction']]
    labeling.to_csv("data/labeling/images.csv", index=True, index_label="ID")


def create_folders():
    if not os.path.exists("data/labeling"):
        os.mkdir("data/labeling")

create_folders()
data = pickle.loads(
    open(input_file, "rb").read())
data = pd.DataFrame(data)
create_labeling_images(data)
image_paths = data["image_path"].tolist()
list_metadata = create_list_metadata(descriptive_metadata)
combine_data(image_paths, list_metadata)

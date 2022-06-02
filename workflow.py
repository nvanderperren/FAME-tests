#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.detect import *
from scripts.encode import *
from scripts.cluster_and_predict import *
import os

treshold = 0.7
csv_file = "data/filenames.csv" # path to csv containing file names and person names per picture

def create_folders():
    if not os.path.exists("data"):
        os.makedirs("data/faces")
        os.makedirs("data/pickle")
        os.makedirs("data/clusters")



def main():
    print("[INFO] workflow started")
    create_folders()
    detect_and_crop(csv_file, treshold)
    encoding()
    cluster_and_predict()
    print("[INFO] workflow ended")

# main
main()

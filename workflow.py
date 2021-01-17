#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.get_metadata import *
from scripts.detect import *
from scripts.encode import *
from scripts.cluster_and_predict import *
import os

# add directories to production folders (remove the '#' in front of relevant directories)
production_dirs = [
    #"/Volumes/UNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/0_Archief"
    #"Images/Images"
]

# add directories to portret folders (remove the '#' in front of relevant directories)
portret_dirs = [
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/3_Portretten",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering/Jerôme de Perlinghi Kunstenaarsportretten Kaaitheater 1977-1997",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering/Fotomaterial Personen",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/1_TeIntegrerenInArchief/portretten",
    #"/VolumesKUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/1_TeIntegrerenInArchief/Auteursportretten_"
    #"Images/People/3_Portretten",
    #"Images/People/Fotomaterial Personen"
]

treshold = 0.7


def create_folders():
    if not os.path.exists("data"):
        os.makedirs("data/faces")
        os.makedirs("data/pickle")
        os.makedirs("data/clusters")


def main():
    print("[INFO] workflow started")
    create_folders()
    create_metadata(production_dirs, portret_dirs)
    detect_and_crop(treshold)
    encoding()
    cluster_and_predict()
    print("[INFO] workflow ended")

main()

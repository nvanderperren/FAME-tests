#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from scripts.get_metadata import *

# add directories to production folders (remove the '#' in front of relevant directories)
production_dirs = [
    #"/Volumes/UNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/0_Archief"
    "Images/Images"
]

# add directories to portret folders (remove the '#' in front of relevant directories)
portret_dirs = [
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/3_Portretten",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering/Jerôme de Perlinghi Kunstenaarsportretten Kaaitheater 1977-1997",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering/Fotomaterial Personen",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/1_TeIntegrerenInArchief/portretten",
    #"/Volumes/KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/1_TeIntegrerenInArchief/Auteursportretten_"
    "Images/People/3_Portretten",
    "Images/People/Fotomaterial Personen"
]

def create_folders():
    if not os.path.exists("data"):
        os.makedirs("data/faces")
        os.makedirs("data/pickle")
        os.makedirs("data/clusters")

# main
create_folders()
create_metadata(production_dirs, portret_dirs)

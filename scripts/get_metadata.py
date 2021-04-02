#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports
import os
import csv

# variables
portret_folder_1 = "Jerôme de Perlinghi Kunstenaarsportretten Kaaitheater 1977-1997"
portret_folder_2 = "Fotomaterial Personen"

# functions


def list_files(dirs):
    r = []
    for dir in dirs:
        print("[INFO] analysing " + str(dir))
        for root, dirs, files in os.walk(dir):
            for name in files:
                path = os.path.join(root, name)
                # print(str(path))

                # Check if file is image and does not start with .
                dirs = path.split('/')
                filename = dirs[-1]
                # Only images, not othet types of files
                if not filename.startswith(".") and filename.endswith(('.jpg', '.JPG', '.tiff', '.png', '.tif', '.eps', '.gif')):
                    # print(path)
                    r.append(path)
    return r


# Method to create map of names with a list of images
def list_people(productions, portrets):
    image_paths_productions = list_files(productions)
    image_paths_portrets = list_files(portrets)
    csv_rows = [["image_path", "name"]]
    names = []
    productions = 0
    name = 'unknown'

    for image_path in image_paths_productions:
        if not (portret_folder_1 in image_path or portret_folder_2 in image_path):
            csv_rows.append([image_path, name])
            productions += 1

    print("[INFO] number of production images: " +
          str(productions))

    '''
    for image_path in image_paths_portrets:
        rest = image_path.split('/')
        rest = rest[rest.index("People")+2:]

        if len(rest) > 1:
            name = rest[0]
        if "namen d" in name.lower():
            name = rest[2]
        elif "namen" in name.lower():
            name = rest[1]
        if name.endswith("_"):
            name = name[:-1]
        if not name in names:
            names.append(name)

        csv_rows.append([image_path, name])
    '''        

    for image_path in image_paths_portrets:
        rest = image_path.split('/')
        if "3_Portretten" in rest:
            rest = rest[6:]
        else:
            rest = rest[7:]

        if len(rest) > 1:
            name = rest[0]
            if "namen d" in name.lower():
                name = rest[2]
            elif "namen" in name.lower():
                name = rest[1]
        if name.endswith("_") or name.endswith(")"):
            name = name[:-1]
        if not '.jpg' in name and not '&' in name:
            csv_rows.append([image_path, name])
            if not name in names:
                names.append(name)
        else:
            csv_rows.append([image_path, 'unknown'])

    print("[INFO] number of portret images: " + str(len(image_paths_portrets)))
    print("[INFO] number of people: " + str(len(names)))

    with open("data/filenames.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_rows)
    csvfile.close()
    print("[INFO] csv stored in data/filenames.csv")


def create_metadata(dirs_productions, dirs_portrets):
    print("[INFO] Creation file names csv started")
    list_people(dirs_productions, dirs_portrets)
    print("[INFO] creation csv ended")

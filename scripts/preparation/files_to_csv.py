from os import path, listdir
import csv
import pandas as pd
from sys import argv

folder=argv[2]
csv_file=argv[1]
output=argv[3]
data = {}
files = [["path", "name", "QID"]]

def load_data(csv_file):
    input_file = open(csv_file, 'r')
    reader = csv.DictReader(input_file)
    for row in reader:
        data[row['QID']] = row['persoon']
    input_file.close()

def get_person(QID):
    try:
        name = data[QID]
    except:
        name = "ONTBREEKT"
    print(name)
    return name

def write_csv(lines):
    output_csv = open(output, 'w')
    writer = csv.writer(output_csv)
    writer.writerows(lines)


load_data(csv_file)

parent_folder = path.basename(folder)
for filepath in listdir(folder):
    parent = path.join(parent_folder, filepath)
    #print(parent)
    if path.isdir(path.join(folder, filepath)):
        if filepath.endswith('_2'):
            QID = filepath[:-2]
        else:
            QID = filepath
        #print(QID)
        name = get_person(QID)
        for file in listdir(path.join(folder, filepath)):
            #print(file)
            files.append([path.join(parent, file), name, QID])

    else:
        QID = filepath.split('.')[0]
        if '_' in QID:
            QID = QID.split('_')[0]
        name = get_person(QID)
        files.append([parent, name, QID])

write_csv(files)
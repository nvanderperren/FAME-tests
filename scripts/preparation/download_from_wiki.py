import os
import csv
from sys import argv

metadata = argv[1]
output_dir = argv[2]

def get_filename(qid, image):
    extension = get_extension(image)
    filename = qid + extension
    i = 2
    while os.path.exists(filename):
        filename = qid + '_' + str(i) + extension
        i = i + 1
    return filename

def get_extension(file):
    if file.endswith('.jpg'):
        return '.jpg'
    else:
        return '.png'

with open(metadata, 'r') as input_file:
    reader = csv.DictReader(input_file)
    os.chdir(output_dir)
    for row in reader:
        afbeelding = row['afbeelding']
        filename = get_filename(row['QID'], afbeelding)
        command = 'wikiget \"{}\" -o {}'.format(afbeelding, filename)
        print(command)
        os.system(command)
    input_file.close()


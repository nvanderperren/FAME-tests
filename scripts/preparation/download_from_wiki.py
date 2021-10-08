import os
import csv
from sys import argv

metadata=argv[1] # csv with columns 'image' and 'QID'
output_dir=argv[2] # absolute path to folder for storing all images

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

def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder

def start(metadata, output_dir):
    with open(metadata, 'r') as input_file:
        reader = csv.DictReader(input_file)
        os.chdir(output_dir)
        for row in reader:
            #os.chdir(output_dir)
            image = row['image']
            if not image == '':
                #os.chdir(create_folder(row['QID']))
                filename = get_filename(row['QID'], image)
                command = 'wikiget \"{}\" -o {}'.format(image,filename)
                #command = 'wikiget \"{}\"'.format(image)
                print(command)
                os.system(command)
        input_file.close()

start(metadata, output_dir)
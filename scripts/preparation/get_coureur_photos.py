import os
from subprocess import run
import csv
from sys import argv

metadata=argv[1] # csv with columns 'category' and 'QID'
output_dir=argv[2] # absolute path to folder for storing all images
CYCLINGARCHIVES = 'cyclingarchives'
PROCYCLINGSTATS = 'procyclingstats'

# could be more DRY

def download_images_cyclingarchives(reader):
    for row in reader:
        cycling_id = row[CYCLINGARCHIVES]
        qid = row['QID']
        if not cycling_id == '':
            run(["dewielersite_image_downloader.sh", cycling_id, qid], shell=True)

def download_images_procyclingstats(reader):
    for row in reader:
        cycling_id = row[PROCYCLINGSTATS]
        qid = row['QID']
        if not cycling_id == '':
            run(["procyclingstats_image_downloader.sh", cycling_id, qid], shell=True)                 


def start(metadata, output_dir):
    os.chdir(output_dir)       
    with open(metadata, 'r') as input_file:
        reader = csv.DictReader(input_file)
        if CYCLINGARCHIVES in reader.fieldnames:
            download_images_cyclingarchives(CYCLINGARCHIVES, reader)
        if PROCYCLINGSTATS in reader.fieldnames:
            download_images_procyclingstats(PROCYCLINGSTATS, reader)

        input_file.close()

start(metadata, output_dir)
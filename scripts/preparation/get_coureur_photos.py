import os
from subprocess import run
import csv
from sys import argv

metadata=argv[1] # csv with columns 'category' and 'QID'
output_dir=argv[2] # absolute path to folder for storing all images
CYCLINGARCHIVES = 'cyclingarchives'
PROCYCLINGSTATS = 'procyclingstats'

# could be more DRY

def download_images_cyclingarchives(cycling_id, output_folder):
    if not cycling_id == '':
        #print(cycling_id)
        run(["/Users/nastasia/Developer/image_recognition/FAME-tests/scripts/preparation/dewielersite_image_downloader.sh", cycling_id, output_folder])

def download_images_procyclingstats(cycling_id, output_folder):
    if not cycling_id == '':
        run(["/Users/nastasia/Developer/image_recognition/FAME-tests/scripts/preparation/procyclingstats_image_downloader.sh", cycling_id, output_folder])                 


def start(metadata, output_dir):       
    with open(metadata, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            qid = row['QID']
            output_folder = '{}/{}'.format(output_dir, qid)
            #print(output_folder)
            if CYCLINGARCHIVES in reader.fieldnames:
                cycling_id = row['cyclingarchives']
                #print(cycling_id)
                download_images_cyclingarchives(cycling_id, output_folder)
            if PROCYCLINGSTATS in reader.fieldnames:
                cycling_id = row['procyclingstats']
                #print(cycling_id)
            #    download_images_procyclingstats(cycling_id, output_folder)

        input_file.close()

start(metadata, output_dir)
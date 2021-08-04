import os
from subprocess import run
import csv
from sys import argv

metadata=argv[1] # csv with columns 'category' and 'QID'
output_dir=argv[2] # absolute path to folder for storing all images

# csv inlezen en QID en cyclig eruithalen
# met deze gegevens commons_category_downloader.sh laten lopen
# spaties er ook uithalen
# klaar?

def start(metadata, output_dir):
    os.chdir(output_dir)       
    with open(metadata, 'r') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            archive_id = row['cyclingarchives']
            QID = row['QID']
            if not archive_id == '':
                #filename = get_filename(row['QID'], image)
                #command = 'wikiget \"{}\" -o {}'.format(afbeelding,filename)
                run(["dewielersite_image_downloader.sh", archive_id, QID], shell=True)
        input_file.close()

start(metadata, output_dir)
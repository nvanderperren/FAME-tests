import os
import csv
from sys import argv
import subprocess

metadata = argv[1]
output_dir = argv[2]

with open(metadata, 'r') as input_file:
    reader = csv.DictReader(input_file)
    os.chdir(output_dir)
    for row in reader:
        command = 'wikiget \"{}\" -o {}'.format(row['afbeelding'], row['filename'])
        print(command)
        os.system(command)
    input_file.close()


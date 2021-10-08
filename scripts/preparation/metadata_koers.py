# TODO: filename bestaat uit filmnummer (4 cijfers) en raamnummer (3 cijfers)
# TODO: leading zeroes verwijderen
# of omgekeerd te werk gaan en vertrekken vanuit de metadata?
# TODO: metadata gebruiken om zo de combi te maken
# TODO: in metadata de van ... en tot ... eruit halen

from csv import DictReader, writer
from datetime import datetime
from sys import argv

metadata_csv=argv[1]
files_csv=argv[2]
erfgoedinzicht = "data/prep_KOERS/erfgoedinzicht.csv"
path_and_metadata = []
paths = {}
metadata = {}
erfgoedinzicht_persons = {}

KOLOM_VAN='nummer negatieven (van)'
KOLOM_TOT='nummer negatieven (tot)'
KOLOM_METADATA='hoofdthema onderwerpen + jaartal'
KOLOM_DATUM='datum'
KOLOM_PERSOON='object_content_person'
HOOFDMAP='NEGT'

def create_metadata_dict():
    input_file = open(metadata_csv, 'r')
    reader = DictReader(input_file)
    for row in reader:
        van=row[KOLOM_VAN]
        tot=row[KOLOM_TOT]
        metadata_line=[row[KOLOM_METADATA],row[KOLOM_DATUM]]
        if not (van == '' or tot == ''):
            for i in range(int(van), int(tot)+1):
                fotomap=row['pagina nummer'].replace('R', '')
                fotomap=fotomap.zfill(4)
                i=str(i).zfill(3)
                key='{}{}{}.jpg'.format(HOOFDMAP,fotomap, i)
                #print(key)
                metadata[key]=metadata_line

    input_file.close()

def create_path_dict():
    input_file = open(files_csv, 'r')
    reader = DictReader(input_file)
    for row in reader:
        filename = row['filename']
        key = filename.split('/')[-1]
        paths[key] = filename

def create_erfgoedinzicht_dict():
    input_file = open(erfgoedinzicht, 'r')
    reader = DictReader(input_file)
    for row in reader:
        key = row['filename']
        erfgoedinzicht_persons[key] = row[KOLOM_PERSOON]

def combine():
    create_path_dict()
    create_metadata_dict()
    create_erfgoedinzicht_dict()
    for key in paths.keys():
        person = ''
        if key in erfgoedinzicht_persons.keys():
            person = erfgoedinzicht_persons[key]
        if key in metadata.keys():
            line = [paths[key], key[:-4]]
            line.extend(metadata[key])
            line.append(person)
            #print(line)
            path_and_metadata.append(line)
        else:
            path_and_metadata.append([paths[key], '', '','', person])



path_and_metadata.append(["path", "object_number", "titel", "datum", "afgebeeld_persoon"])
combine()
#print(path_and_metadata)
with open('koers_metadata.csv', 'w') as output_file:
    csv_writer = writer(output_file)
    csv_writer.writerows(path_and_metadata)
#print(paths)
#print(len(paths))
# TODO: filename bestaat uit filmnummer (4 cijfers) en raamnummer (3 cijfers)
# TODO: leading zeroes verwijderen
# of omgekeerd te werk gaan en vertrekken vanuit de metadata?
# TODO: metadata gebruiken om zo de combi te maken
# TODO: in metadata de van ... en tot ... eruit halen

from csv import DictReader, writer
from sys import argv

csv=argv[1]
metadata = {}
KOLOM_VAN='nummer negatieven (van)'
KOLOM_TOT='nummer negatieven (tot)'
KOLOM_METADATA='hoofdthema onderwerpen + jaartal'
HOOFDMAP='NEGT'

input_file = open(csv, 'r')
reader = DictReader(input_file)
for row in reader:
    van=row[KOLOM_VAN]
    tot=row[KOLOM_TOT]
    metadata_line=row[KOLOM_METADATA]
    if not (van == '' or tot == ''):
        for i in range(int(van), int(tot)+1):
            fotomap=row['pagina nummer'].replace('R', '')
            fotomap=fotomap.zfill(4)
            i=str(i).zfill(3)
            key='{}{}{}.jpg'.format(HOOFDMAP,fotomap, i)
            metadata[key]=metadata_line

input_file.close()
print(metadata)
print(len(metadata))
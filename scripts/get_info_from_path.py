#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import re

# meestal vier elementen in de vorm: producer, seizoen, titel
# maar soms kan het ook 1 zijn: skippen, heeft niets,
# soms is het ook locatie, seizoen, titel
# als het er maar drie zijn, dan is het meestal: organisatie, titel,

def remove_chars(word):
    if word.endswith('_'):
        word = word[-1]

    if '_' in word:
        names = word.split('_')
        word = names[0]

    return word


def write_line(line):
    with open('productions.csv', 'a') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(line)
    write_file.close()



def get_info_from_path(path):
    theaterseizoen =''
    productietitel = ''
    podiumkunstengezelschap = ''
    person = ''

    line = []

    dirs = path.split('/')
    info = dirs[6:]

    #print("busy with {} with length {}".format(path, str(len(info))))

    if not ('portretten' in path.lower() or 'fotomaterial personen' in path.lower()):
        person = ''     

        # if len(info) > 3

        if len(info) > 3:
            podiumkunstengezelschap = info[0]
            theaterseizoen = info[1]
            productietitel = info[2]

            # find correct sequence
            a = re.match("\d\d\d\d-\d\d\d\d", theaterseizoen)
            b = re.match("\d\d-\d\d", theaterseizoen)
            c = re.match("\d\d\d\d", theaterseizoen)
            
            if "onbekend" in theaterseizoen.lower() or "algemeen" in theaterseizoen.lower() or "unknown" in theaterseizoen.lower():
                theaterseizoen = ''         
            elif a is None and b is None and c is None:
                productietitel = info[1]
                theaterseizoen = info[2]

            # cleanups
            if "onbekend" in theaterseizoen.lower() or "algemeen" in theaterseizoen.lower() or "unknown" in theaterseizoen.lower():
                theaterseizoen = ''

            if podiumkunstengezelschap == "Koninklijk Ballot van Vlaanderen":
                podiumkunstengezelschap = "Koninklijk Ballet van Vlaanderen"

            ##  exceptinos
            if len(info) == 6 and "theater aan zee" in productietitel.lower():
                productietitel = info[3]

            if len(info) == 5 and productietitel.lower() == "producties":
                productietitel = info[3]

            if len(info) == 5 and podiumkunstengezelschap == 'BENT':
                podiumkunstengezelschap = info[1]
                productietitel = info[3]

            if len(info) == 4 and productietitel == "Ballet Royal de Wallonie":
                productietitel = info[0]
                podiumkunstengezelschap = info[1]

        elif len(info) == 2:
            podiumkunstengezelschap = info[0]

        elif len(info) == 3:
            podiumkunstengezelschap = info[0]
            theaterseizoen = info[1]

            a = re.match("\d\d\d\d-\d\d\d\d", theaterseizoen)
            b = re.match("\d\d-\d\d", theaterseizoen)
            c = re.match("\d\d\d\d", theaterseizoen)

            if a is None and b is None and c is None:
                productietitel = theaterseizoen
                theaterseizoen = ''
    
    else:
        if (len(info)) > 1:
            person = info[1]

            if 'namen ' in person.lower():
                person = info[2]
        
    line = [path, remove_chars(podiumkunstengezelschap), remove_chars(productietitel), theaterseizoen, person]
    write_line(line)

with open('productions.csv', 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['path', 'organisatie', 'productie', 'seizoen', 'person'])
output_file.close()

with open('data/filenames.csv', 'r') as read_file:

    content = csv.DictReader(read_file)
    count = 0

    for row in content:
        print(str(count))
        if row['name'] == 'unknown':
            get_info_from_path(row['image_path'])
        else:
            person = row['name']
            path = row['image_path']
            line = [path, '', '', '', person]
            write_line(line)
        count += 1

read_file.close()

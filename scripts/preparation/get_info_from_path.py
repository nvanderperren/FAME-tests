#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import re

# combineren met een andere CSV
# searchterm gebruiken
# opzoeken en dan via CSV DictReader kunstenpunt_id, company QID en productie QID ophalen

OUTPUT_FILENAME = "kunstenpunt_data.csv"
IDENTIFIERS_CSV = "identifiers_KP.csv"
FILENAMES_CSV = "data/filenames.csv"

# cleanup metadata
def remove_chars(word):
    if word.endswith('_'):
        word = word[-1]

    if '_' in word:
        names = word.split('_')
        word = names[0]

    return word

# retrieve the century (19 or 20) of a year
def get_century(year):
    if int(year) > 20:
        return "19" + year
    else:
        return "20" + year
    
# return season in format YYYY-YYYY where possible
def beautify_season(season):
    if season == '':
        return ''

    if not season[:2].isdigit():
        return season

    if len(season) < 9:
        start = season[:2]
        if len(season) == 5:
            end = season[3:]
            
            season = get_century(start) + '-' + get_century(end) 
        elif len(season) == 7:
            season = get_century(season[:2]) + season[2:]

        elif len(season) == 8:
            mid = season[3:5]
            end = season[6:]
            season = get_century(start) + '-' + get_century(mid) + '-' + get_century(end)

        elif len(season) == 2:
            season = get_century(season)
    
    return season

# get the searchterm used in the identifiers csv file
def get_searchterm(production, season):
    if production == '' or season == '':
        return
    
    searchterm = production + " (" + season + ")"
    return searchterm

# write infos in csv
def write_line(line):
    with open(OUTPUT_FILENAME, 'a') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(line)
    write_file.close()

# get identifiers (QID's, KP ID) in other csv_file
def find_identifiers_from_csv(searchterm):
    company_qid = ''
    production_qid = ''
    kunstenpunt_id = ''
    with open(IDENTIFIERS_CSV, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            if row['searchterm'] == searchterm:
                company_qid = row['production_wiki_id']
                production_qid = row['wikidata_id']
                kunstenpunt_id = row['kunstenpunt_id'].split('.')[0]
        
    input_file.close()
    return {"company_qid": company_qid, "production_qid": production_qid, 
    "kunstenpunt_id": kunstenpunt_id}
    
    
# method to get info from path of image
def get_info_from_path(path):
    theaterseizoen =''
    productietitel = ''
    podiumkunstengezelschap = ''
    person = ''
    company_qid = ''
    production_qid = ''
    kunstenpunt_id = ''

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
    
        # cleanup
        theaterseizoen = beautify_season(theaterseizoen)
        podiumkunstengezelschap = remove_chars(podiumkunstengezelschap)
        productietitel = remove_chars(productietitel)

    else:
        if (len(info)) > 1:
            person = info[1]

            if 'namen ' in person.lower():
                person = info[2]



    search_term = get_searchterm(productietitel, theaterseizoen)
    if search_term is not None:
        if not search_term in identifiers.keys():
            list_identifiers = find_identifiers_from_csv(search_term)
            identifiers[search_term] = list_identifiers
    
        company_qid = identifiers[search_term]["company_qid"]
        production_qid = identifiers[search_term]["production_qid"]
        kunstenpunt_id = identifiers[search_term]["kunstenpunt_id"]

       
    line = [path, podiumkunstengezelschap, productietitel, theaterseizoen, person, 
    company_qid, production_qid, kunstenpunt_id]
    write_line(line)
    

## main

with open(OUTPUT_FILENAME, 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['path', 'organisatie', 'productie', 'seizoen', 'persoon', 'gezelschap_QID', 
    'productie_QID', 'kunstenpunt_ID'])
output_file.close()


with open(FILENAMES_CSV, 'r') as read_file:

    identifiers = {}

    content = csv.DictReader(read_file)
    count = 0

    for row in content:
        if row['name'] == 'unknown':
            get_info_from_path(row['image_path'])
        else:
            person = row['name']
            path = row['image_path']
            line = [path, '', '', '', person, '', '', '']
            write_line(line)
        count += 1

read_file.close()
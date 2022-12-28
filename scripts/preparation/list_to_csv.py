# lees het bestand in
# splits het op
# check of er een punt in het tweede deel zit
# indien niet, dan is de directory de QID
# indien wel, dan is het deel voor de punt de QID

from csv import DictReader, writer
import re
from sys import argv


reference_list = argv[1]
authorities = argv[2]
output = argv[3]
data = {}
lines = [["path", "name", "QID"]]


def load_data(csv_file: str) -> None:
    input_file = open(csv_file, 'r')
    reader = DictReader(input_file)
    for row in reader:
        data[row['QID']] = row['persoon']
    input_file.close()

def get_person(QID: str) -> str:
    try:
        name = data[QID]
    except:
        name = "ONTBREEKT"
    print(name)
    return name


def read_reference_list(list:str) -> None:
    with open(list, 'r') as reference_file:
        
        for line in reference_file.readlines():
            qid = line.split('/')[1]
            if (re.search('\.[a-zA-Z]+$', qid)):
                qid = qid.split('.')[0]
            if '_' in qid:
                qid = qid.split('_')[0]
            name = get_person(qid)
            path = clean_path(line)
            lines.append([path, name, qid])

        reference_file.close()


def write_csv(lines) -> None:
    with open(output, 'w') as output_csv:
        csv_writer = writer(output_csv)
        csv_writer.writerows(lines)

def clean_path(path: str) -> str:
    path = path.replace('\n', '')
    path = path.replace('"', '')
    return path

def start() -> None:
    load_data(authorities)
    read_reference_list(reference_list)
    print(len(lines)-1)
    write_csv(lines)

start()
        
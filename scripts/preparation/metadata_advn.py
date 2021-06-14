import csv

photos='data/prep_advn/foto.csv'
portrets='data/prep_advn/portretten.csv'
subjects='data/prep_advn/onderwerpen.csv'

#doel: aan de bestandsnamen moet een naam of een onderwerp gekoppeld worden
#vervelend: naam en portret is gekoppeld aan meerdere mappen die in meerdere koloms zitten
#dus: die moeten we eruit halen
#werken met een dictionary?

paths = []
person_columns = ['Persoon', 'QID', 'Vlaams Parlement ID', 'Belgische Senaat ID']
subject_columns = ['Map', 'Onderwerp']

def create_dict_data(file, columns):
    count_columns = len(columns)
    data = {}
    with open(file, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            line = []
            for i in range(count_columns):
                line.extend([row[columns[i]]])
            #line = [row[columns[0]],row[columns[1]]]
            if row['VFA']:
                key = row['VFA'].split('/', 1)[0]
                data[key] = line
            if row['VFB']:
                key = row['VFB'].split('/', 1)[0]
                data[key] = line
            if row['VFC']:
                key = row['VFC'].split('/', 1)[0]
                data[key] = line
    input_file.close()
    return data


def create_dict_paths(file):
    with open(file, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        for row in csv_reader:
            key = row['path'].split('/')[1]
            subkeys = key.split('_')
            subkeys[1] = subkeys[1].lstrip('0')
            key = "{}_{}".format(subkeys[0], subkeys[1])
            paths.append([key, row['path']])
    input_file.close()

def combine_metadata_paths(data):
    lines = []
    for path in paths:
        key = path[0]
        if key in data:
            line = [path[1]]
            line.extend(data[key])
            lines.append(line) 
    return lines


def write_file(filename, columns, data):
    columns.insert(0, 'path')
    with open('data/prep_advn/{}.csv'.format(filename), 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(columns)
        writer.writerows(data)
    output_file.close()

data_portrets = create_dict_data(portrets, person_columns)
data_subjects = create_dict_data(subjects, subject_columns)
create_dict_paths(photos)
#write_file(data)
portret_lines = combine_metadata_paths(data_portrets)
subject_lines = combine_metadata_paths(data_subjects)
write_file('portrets', person_columns, portret_lines)
write_file('subjects', subject_columns, subject_lines)

#print(subject_lines)

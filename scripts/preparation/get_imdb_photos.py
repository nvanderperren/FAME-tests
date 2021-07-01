from imdb import IMDb
from csv import DictReader
from os import chdir
import requests
from sys import argv

metadata = argv[1]
output_dir = argv[2]
imdb = IMDb()

def get_image(code):
    if not code.isdigit():
        id = code[2:]
    else:
        id = code
    person = imdb.get_person(id)
    name = person['name']
    image = None
    try:
        image = person['full-size headshot']
    except:
        print("{} has no image".format(name))
    finally:
        print("{} has an image".format(name))
    return image

def download_image(url, filename):
    with requests.get(url, stream=True) as image:
        with open(filename, "wb") as f:
            for chunk in image.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.close()
        image.close()

with open(metadata, 'r') as input_file:
    reader = DictReader(input_file)
    chdir(output_dir)
    for row in reader:
        image = get_image(row['IMDb'])
        filename = row['QID'] + '.jpg'
        if image:
            download_image(str(image), filename)
    input_file.close()
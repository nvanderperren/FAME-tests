#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports face encoding
from pyfacy import utils
from PIL import Image
from io import BytesIO
import base64
import cv2
import pickle
import pandas as pd
import csv

# Function to create embeddable images for visualisation
# needs aan image


def embeddable_image(image):
    # img_data = 255 - 15 * data.astype(np.uint8)
    image = Image.fromarray(image, mode='L').resize((64, 64), Image.BICUBIC)
    buffer = BytesIO()
    image.save(buffer, format='png')
    for_encoding = buffer.getvalue()
    return 'data:image/png;base64,' + base64.b64encode(for_encoding).decode('utf-8')


def resize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    scale_percent = 50  # percent of original size, use if you need to downsample
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
    return resized

def get_face_location(data):
    data = data.lstrip('(').rstrip(')')
    data = data.split(',')
    face_location = (int(data[0]), int(data[1]),
                                  int(data[2]), int(data[3]))
    return face_location


def get_face(image_path, face_location):
    image = cv2.imread(image_path)
    (top, right, bottom, left) = face_location
    cropped_image = image[top:bottom, left:right]
    return cropped_image


def encoding_faces():
    lines = []
    # better work with pickle files, then we don't need to modify the face string
    with open("data/found-faces.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        print("[INFO] quantifying faces...")

        for index, row in enumerate(reader):
            print("- encode face nr. " + str(index+1))
            image_path = row['image_path']
            person = row['name']
            face_location_data = row['face_location']
            face_location = get_face_location(face_location_data)
            try:
                cropped_image_data = get_face(image_path, face_location)
                encoding = utils.img_to_encodings(cropped_image_data)
                if len(encoding) > 0:
                    resized_image = resize_image(cropped_image_data)
                    face_encoding = embeddable_image(resized_image)
                    data = [{"image_path": image_path, "name": person, "face_location": face_location,
                    "face_encoding": encoding[0], "image": face_encoding}]
                    lines.extend(data)
            except:
                print("[ERROR] could not open image {}, skipping...".format(image_path))

    return lines

def write_data(filename,data):
    f = open('data/pickle/' + filename + '.pickle', 'wb')
    f.write(pickle.dumps(data))
    f.close()

def encoding():
    print("[INFO] Step 2: Encoding faces...")
    data = encoding_faces()
    print("[INFO] serializing encodings...")
    write_data('face_encoding', data)
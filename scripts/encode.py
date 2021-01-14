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


def get_face(image_path, face_location):
    image = cv2.imread(image_path)
    face_location = face_location.lstrip('(').rstrip(')')
    face_location = face_location.split(',')
    (top, right, bottom, left) = (int(face_location[0]), int(face_location[1]),
                                  int(face_location[2]), int(face_location[3]))
    cropped_image = image[top:bottom, left:right]
    return cropped_image


def encode(image_path, face_location, line):
    cropped_image = get_face(image_path, face_location)
    encoding = utils.img_to_encodings(cropped_image)
    if len(encoding) > 0:
        resized_image = resize_image(cropped_image)
        face_encoding = embeddable_image(resized_image)
        line.append(encoding)
        line.append(face_encoding)
    return line


def encoding_faces():
    lines = []
    # better work with pickle files, then we don't need to modify the face string
    with open("../data/found-faces.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        print("[INFO] quantifying faces...")

        for index, row in enumerate(reader):
            print("- encode file nr. " + str(index+1))
            image_path = row['path']
            person = row['name']
            face_location = row['face_location']
            cropped_image = row['crop']
            line = [image_path, person, face_location, cropped_image]
            line = encode(image_path, face_location, line)
            lines.append(line)
    
    return lines

def write_data(filename,data):
    f = open(filename + '.pickle', 'wb')
    f.write(pickle.dumps(data))
    f.close()
    data.to_csv(filename + '.csv', index=False)

data = encoding_faces()
print("[INFO] serializing encodings...")
data = pd.DataFrame(data,columns=["path", "name", "face_location",
              "crop", "face_encoding", "image_encoding"])
write_data("../data/face_encoding", data)

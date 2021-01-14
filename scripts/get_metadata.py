# imports
import os
import csv

# variables
dirs_productions = []
dirs_portrets = []
'''
dirs_productions.append(
    "/Volumes/UNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering")
dirs_productions.append(
    "KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/0_Archief")

dirs_portrets.append(
    "KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/3_Portretten")
dirs_portrets.append("KUNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering/Jerôme de Perlinghi Kunstenaarsportretten Kaaitheater 1977-1997")
dirs_portrets.append("KUNSTENPUNT FOTOCOLLECTIE/TEMP BACKUP ZUENA FOTO SCANS VTI 20191125/digitalisering/Fotomaterial Personen")
dirs_portrets.append(
    "KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/1_TeIntegrerenInArchief/portretten")
dirs_portrets.append("KUNSTENPUNT FOTOCOLLECTIE/BACKUP VTi fotocollectie digital born/1_TeIntegrerenInArchief/Auteursportretten_")
'''
portret_folder_1 = "Jerôme de Perlinghi Kunstenaarsportretten Kaaitheater 1977-1997"
portret_folder_2 = "Fotomateriaal Personen"

dirs_productions.append("../Images/Images")
dirs_portrets.append("../Images/People/3_Portretten")
dirs_portrets.append("../Images/People/Fotomaterial Personen")
# functions


def list_files(dirs):
    r = []
    for dir in dirs:
        for root, dirs, files in os.walk(dir):
            for name in files:
                path = os.path.join(root, name)

                # Check if file is image and does not start with .
                dirs = path.split('/')
                filename = dirs[-1]
                # Only images, not othet types of files
                if not filename.startswith(".") and filename.endswith(('.jpg', '.JPG', '.tiff', '.png', '.tif', '.eps', '.gif')):
                    # print(path)
                    r.append(path)
    return r


# Method to create map of names with a list of images
def list_people():
    image_paths_productions = list_files(dirs_productions)
    image_paths_portrets = list_files(dirs_portrets)
    csv_rows = [["path, name"]]
    names = []

    for image_path in image_paths_productions:
        if portret_folder_1 in image_path or portret_folder_2 in image_path:
            break
        name = "unknown"
        csv_rows.append([image_path, name])
    
    print("[INFO] numer of production images: " + str(len(image_paths_productions)))

    for image_path in image_paths_portrets:
            rest = image_path.split('/')
            rest = rest[rest.index("People")+2:]
            print(rest)

            if len(rest) > 1:
                name = rest[0]
            if "namen d" in name.lower():
                name = rest[2]
            elif "namen" in name.lower():
                name = rest[1]
            if name.endswith("_"):
                name = name[:-1]
            print("Naam: " + name)
            if not name in names:
                names.append(name)

            csv_rows.append([image_path, name])

    print("[INFO] numer of portret images: " + str(len(image_paths_portrets)))
    print("[INFO] number of people: " + str(len(names)))

    if not os.path.exists("../data"):
        os.mkdir("../data")
    
    with open ("../data/filenames.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_rows)
    csvfile.close()
    print("[INFO]: csv stored in ../data/filenames.csv")


print("[INFO] creation file names csv started")
list_people()
print("[INFO] creation file names csv ended")
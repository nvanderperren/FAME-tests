import csv
import pickle
import pandas as pd
import json
import numpy as np

# setup data
data = pickle.loads(open(
"data/pickle/face-clustering-results.pickle", "rb").read())
data = pd.DataFrame(data)
data['correction'] = data['prediction']
data['clusterCorrection'] = data['HDBSCANclusters']

# setup face vote resutls
label_results = json.load(open("face_votes.json", 'r'))
face_corrections = pd.DataFrame(label_results['votes'])
face_corrections = face_corrections['', np.nan]
face_corrections_results = face_corrections[face_corrections.label_text.notnull()]

# if label_text is empty, then it's an error
errors = face_corrections[face_corrections.label_text.isnull()]
for index, row in errors.iterrows():
    id = row['face_id']
    data.at[id, 'correction'] = "error"
print("[INFO] Number of not faces: {}".format(len(errors)))

# go further with the ones that have a label_text
face_corrections_results = face_corrections_results.reset_index(drop=True)

for index, row in face_corrections_results.iterrows():
    # name of the person is a label_text
    # it's also a face_id
    name = row['label_text']
    if "Unknown" in name:
        name = name.replace("unknown", "")
    
    # use face_id
    id = row['face_id']

    if name.isdigit():
        name = int(name)

        # name: het cijfer van de label_text uit face_votes.json
        # id: het cijfer (id) dat aan dat bepaalde gezicht gegeven werd
        if name != id:
            # iloc: geef een rij op basis van index
            # loc: geef een reeks rijen op basis van label of conditionele waardes
            
            # geef rij met index = name en kolom prediction
            # als de voorspelling bij de label_text niet unknown is, maar die bij dat gezciht wel
            if data.iloc[name]['prediction'] != "unknown" and data.iloc[id]['prediction'] == "unknown":
                # dan kan je een correctie geven voor dat face_id en zeggen dat het overeenkomt bij de voorspelling van de label_text
                data.at[id, 'correction'] = data.iloc[name]['prediction']

                # update the clusters als dat face_id tot een  cluster behoort
                if data.iloc[id]['HDBSCAN_clusters'] != -1:
                    # geef rij waarvan HDBSCANclusters == de HDBScancluster op rij met index van het face_id
                    names = data.loc[data['HDBSCAN_clusters'] == data.iloc[id]['HDBSCAN_clusters']]
                    for index, row in names.iterrows():
                        # als de cluster hetzelfde is, dan hebben al die gezichten ook die voorspelde naam van die label_text
                        data.at[index, 'correction'] = data.iloc[name]['prediction']
                else:
                    # als het gezicht niet tot een cluster behoort, dan behoort het tot dat van de label_text
                    data.at[id, 'clusterCorrection'] = data.iloc[name]['clusterCorrection']

            # het kan ook gebeuren dat de voorspelling bij de label_text unknown is,
            # maar dat er wel voorspelling is voor die face_id 
            elif data.iloc[name]['prediction'] == "unknown" and data.iloc[id]['prediction'] != "unknown":
                # geef dan de label_text de voorspelling van de face_id
                data.at[name, 'correction'] = data.iloc[id]['prediction']
                # als de label_text verbonden is met een cluster
                if data.iloc[name]['HDBSCAN_clusters'] != -1:
                    # geef dan alle rijen waarvan de cluster overeenkomt met dat van de label_text
                    names = data.loc[data['HDBSCAN_clusters'] == data.iloc[name]['HDBSCAN_clusters']]
                    for index, row in names.iterrows():
                        # want al deze rijen zouden dezelfde voorspelling moeten krijgen van het face_id
                        data.at[index, 'correction'] = data.iloc[id]['prediction']
                else: # als de label_text wel een cluster heeft
                    # zorg dan dat die dezelfde wordt als die van de face_id
                    data.at[id, 'clusterCorrection'] = data.loc[id]['clusterCorrection']
            
            # zowel label_text als face_id hebben nog geen voorspelling gekregen
            else: # zet ze dan alvast in clusters 
                # als de face_id een cluster heeft, dan geef je die aan allen waar de label_text in voorkomt
                if data.iloc[name]['clusterCorrection'] == -1 and data.iloc[id]['clusterCorrection'] != -1:
                    data.at[name, 'clusterCorrection'] = data.iloc[id]['clusterCorrection']
                 # en omgekeerd
                elif data.iloc[name]['clusterCorrection' ] != -1 and data.iloc[id]['clusterCorrection'] == -1:
                    data.at[id, 'clusterCorrection'] = data.iloc[name]['clusterCorrection']

    # als naam geen nummer is, dan is het een nieuwe naam
    else:
        data.at[id, 'correction'] = name

        # zoek in de data alle rijen met voorspellingen met dezelfde naam
        same_names = data.loc[data['prediction'] == name]

        for index, row in same_names.iterrows():
            if data.iloc[id]['clusterCorrection'] == -1 and row['clusterCorrection'] != -1:
                data.at[index, 'clusterCorrection'] = row['clusterCorrection']
            else:
                if row['clusterCorrection'] == -1:
                    data.at[index, 'clusterCorrection'] = data.iloc[id]['clusterCorrection']
                
        if data.iloc[id]['prediction'] != "unknown":
            same_names = data.loc[data['prediction'] == data.iloc[id]['prediction']]
            for index, row in same_names.iterrows():
                data.at[index, 'correction'] = name
        
        if data.iloc[id]['clusterCorrection'] != -1:
            same_clusters = data.loc[data['clusterCorrection'] == data.iloc[id]['clusterCorrection']]
            for index, row in same_clusters.iterrows():
                data.at[index, 'correction'] = name
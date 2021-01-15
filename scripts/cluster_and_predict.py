import pickle
import pandas as pd
import numpy as np
import cv2
from imutils import build_montages
import matplotlib.pyplot as plt

# imports clustering
import hdbscan
import umap
import umap.plot
from sklearn import neighbors
from sklearn.neighbors import NearestNeighbors

from bokeh.io import output_notebook
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper
from bokeh.palettes import Spectral10, Turbo256, Plasma256, plasma

# imports fuzzy matching
from fuzzywuzzy import process


def cluster_faces(data):
    print("[INFO] clustering using HDBSCAN algorithm")
    ids = pd.DataFrame({'name': data.name.unique(),
                    'personID': range(len(data.name.unique()))})
    data = data.merge(ids, on='name', how='left')
    print(data['face_encoding'])
    encodings = data['face_encoding'].tolist()

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=2, min_samples=2, metric='euclidean').fit(encodings) # a cluster must have at least two faces


    labelIDs = np.unique(clusterer.labels_)
    data['HDBSCANclusters'] = clusterer.labels_
    
    data['probability'] = clusterer.probabilities_

    numUniqueFaces = len(np.where(labelIDs > -1)[0])

    data = data.drop('personID', 1)
    print(list(data.columns))
    print(data)
    # data.to_csv(
    #    "drive/My Drive/FaceRecognition/Results/Face_recognition_predictions.csv")

    print("[INFO] # unique faces: {}".format(numUniqueFaces))
    print(str(clusterer.labels_.max()) + ' clusters are found')
    print(len(data.loc[data['HDBSCANclusters'] == -1]), "faces not clustered")
    calculateNeighbors(data, encodings)
    predict(data, clusterer, labelIDs)
    return data
    # visualise_clusters_image(clusterer,labelIDs)
    # visualise_clusters_umap(data)
    


def visualise_clusters_umap(data):
    print("[INFO] preparing UMAP visualisation")
    encodings = data['encodings'].tolist()

    reducer = umap.UMAP(n_neighbors=2, min_dist=0.2,
                    metric='euclidean', random_state=42).fit(encodings)
    embedding = reducer.transform(encodings)
    print(embedding.shape)

    df = pd.DataFrame(embedding, columns=('x', 'y'))
    df['class'] = data['name']
    df['image'] = data['embeddableImage']
    df['clusterID'] = [str(x+1) for x in list(data['HDBSCANclusters'])]
    df['probability'] = data['probability']

    n = len(list(np.unique(data['HDBSCANclusters'])))
    if n < 255:
        pal = plasma(n)
    else:
        pal = Plasma256
    datasource = ColumnDataSource(df)
    color_mapping = CategoricalColorMapper(
        factors=[str(x+1) for x in list(np.unique(data['HDBSCANclusters']))], palette=pal)

    plot_figure = figure(
        title='UMAP projection',
        plot_width=600,
        plot_height=600,
        tools=('pan, wheel_zoom, reset')
    )

    plot_figure.add_tools(HoverTool(tooltips="""
    <div>
        <div>
            <img src='@image'  style='float:left; width:100px;height:100px; margin: 5px 5px 5px 5px'/>
        </div>
        <div>
            <span style='font-size: 12px'>@class</span>
        </div>
        <div>
            <span style='font-size: 12px'>@clusterID</span>
        </div>
        <div>
            <span style='font-size: 12px'>@probability</span>
        </div>
    </div>
    """))

    plot_figure.circle(
        'x',
        'y',
        source=datasource,
        color=dict(field='clusterID', transform=color_mapping),
        line_alpha=0.6,
        fill_alpha=0.6,
        size=4
    )

    output_notebook()
    show(plot_figure)

def visualise_clusters_image(clusterer, labelIDs):
    print("[INFO] preparing visualisation clusters")
    # loop over the unique face integers
    for labelID in labelIDs:
        # find all indexes into the `data` array that belong to the current label ID, then randomly sample a maximum of 25 indexes from the set
        print("[INFO] faces for face ID: {}".format(labelID))
        idxs = np.where(clusterer.labels_ == labelID)[0]
        idxs = np.random.choice(idxs, size=min(25, len(idxs)), replace=False)

        # initialize the list of faces to include in the montage
        faces = []

        # loop over the sampled indexes
        for i in idxs:
            # load the input image and extract the face ROI
            image = cv2.imread(data.at[i, 'path'])
            (top, right, bottom, left) = data.at[i, 'face_location']
            face = image[top:bottom, left:right]

            # force resize the face ROI to 96x96 and then add it to the faces montage list
            face = cv2.resize(face, (96, 96))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

            faces.append(face)
            print(data.at[i, 'path'])

        # create a montage using 96x96 "tiles" with 5 rows and 5 columns
        montage = build_montages(faces, (96, 96), (5, 5))[0]

        fig = plt.figure(figsize=(20, 30))
        plt.imshow(montage)
        # plt.imsave()

def predict(data, clusterer, labelIDs):
    print("[INFO] predicting persons")
    data['prediction'] = data['name']

    for labelID in labelIDs:
        # print("[INFO] faces for face ID: {}".format(labelID))
        idxs = np.where(clusterer.labels_ == labelID)[0]
        # print(idxs)
        if labelID != -1:

            names = []
            for i in idxs:
                name = data.at[i, 'prediction']
                if name != 'unknown':
                    names.append(name)

            # print(len(names))
            if len(np.unique(names)) == 1:
                for i in idxs:
                    data.at[i, 'prediction'] = names[0]
            elif len(names) > 1:
                # check if names are simalarity (other spelling)
                similarity = process.extract(names[0], names)
                # count how many time a name is in a cluster
                count = dict((i, names.count(i)) for i in names)
                # print(similarity, count)

                Keymax = max(count, key=count.get)
                if count[Keymax] > 1:
                    for i in idxs:
                        if data.at[i, 'prediction'] == 'U-unknown':
                            data.at[i, 'prediction'] = Keymax
                else:
                    uniqueNames = []
                    for t in similarity:
                        if t[1] > 80:
                            uniqueNames.append(t[0])
                    if len(names) == len(uniqueNames):
                        #print(names, uniqueNames)
                        for i in idxs:
                            # if data.at[i,'prediction'] == 'Unkown':
                            data.at[i, 'prediction'] = uniqueNames[0]

    print(list(data.columns))
    print("Unknown people before clustering:", (data.name == 'unknown').sum())
    print("Unknown people after clustering:", (data.prediction == 'unknown').sum())

    print(len(data.loc[data['prediction'] == "unknown"]))
    # print(data['data.face_encoding'][0].shape)
    # data.to_pickle(
    #    "drive/My Drive/FaceRecognition/Results/Face-clustering-results.pickle")

def calculateNeighbors(data, encodings):
    print("[INFO] calculating neighbours")
    nbrs = NearestNeighbors(n_neighbors=20, algorithm='ball_tree').fit(encodings)
    distances, indices = nbrs.kneighbors(encodings)
    # print(indices, distances)
    '''
    for i in indices[9]:
    person = data.loc[i, 'name'] 
    cluster = data.loc[i, 'HDBSCANclusters']
    # print(person, cluster)
    '''
    reducer = umap.UMAP(n_neighbors=2, min_dist=0.2,
                        metric='euclidean', random_state=42).fit(encodings)
    embedding = reducer.transform(encodings)
    knn_indices, knn_dists, rp_forest = umap.umap_.nearest_neighbors(
        embedding, n_neighbors=20, metric='euclidean', metric_kwds={}, angular=False, random_state=np.random.RandomState(42))
    # print(knn_indices, knn_dists)
    '''
    for i in knn_indices[9]:
    person = data.loc[i, 'name'] 
    cluster = data.loc[i, 'HDBSCANclusters']
    # print(person, cluster)
    '''

    neighbors = []
    umapneighbors = []
    for i, row in data.iterrows():
        neighbors.append(indices[i].tolist())
        umapneighbors.append(knn_indices[i].tolist())

    data['neighbors'] = neighbors
    data['UMAPneighbors'] = umapneighbors

    cluster = []
    for i, row in data.iterrows():
        c = data.at[i, 'HDBSCANclusters']

        if c != -1:
            lijst = data[data['HDBSCANclusters'] == c].index.tolist()
            cluster.append(lijst)
            #print(i, lijst, namen)
        else:
            lijst = []
            cluster.append(lijst)

    data['clusterList'] = cluster


# main
print("[INFO] loading data for clustering")
data = pickle.loads(open(
    "../data/face_encoding.pickle", "rb").read())
data = pd.DataFrame(data)
print("[INFO] start clustering")
predictions = cluster_faces(data)
print(predictions.columns)
print(predictions)
predictions.to_csv("../data/face-clustering-results.csv")
predictions.to_pickle(
        "../data/face-clustering-results.pickle")


# installed python-Levenshtein
#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import pandas as pd
import numpy as np
import cv2
from imutils import build_montages
import matplotlib.pyplot as plt
import math

# imports clustering
import hdbscan
import umap
import umap.plot
from sklearn import neighbors
from sklearn.neighbors import NearestNeighbors

from bokeh.io import output_notebook, output_file, save
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
    encodings = data['face_encoding'].tolist()

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=2, min_samples=2, metric='euclidean').fit(encodings)  # a cluster must have at least two faces

    labelIDs = np.unique(clusterer.labels_)
    data['HDBSCAN_clusters'] = clusterer.labels_
    data['probability'] = clusterer.probabilities_

    numUniqueFaces = len(np.where(labelIDs > -1)[0])

    data = data.drop('personID', 1)
    # print(data)
    print("[INFO] # unique faces: {}".format(numUniqueFaces))
    print(str(clusterer.labels_.max()) + ' clusters are found')
    print(len(data.loc[data['HDBSCAN_clusters'] == -1]), "faces not clustered")
    calculateNeighbors(data, encodings)
    predict(data, clusterer, labelIDs)
    visualise_clusters_image(data, clusterer,labelIDs)
    visualise_clusters_umap(data)
    return data


def visualise_clusters_umap(data):
    print("[INFO] preparing UMAP visualisation")
    encodings = data['face_encoding'].tolist()

    reducer = umap.UMAP(n_neighbors=2, min_dist=0.2,
                        metric='euclidean', random_state=42).fit(encodings)
    embedding = reducer.transform(encodings)

    df = pd.DataFrame(embedding, columns=('x', 'y'))
    df['class'] = data['name']
    df['image'] = data['image']
    df['clusterID'] = [str(x+1) for x in list(data['HDBSCAN_clusters'])]
    df['probability'] = data['probability']
    df['prediction'] = data['prediction']

    n = len(list(np.unique(data['HDBSCAN_clusters'])))
    if n < 255:
        pal = plasma(n)
    else:
        pal = Plasma256
    datasource = ColumnDataSource(df)
    color_mapping = CategoricalColorMapper(
        factors=[str(x+1) for x in list(np.unique(data['HDBSCAN_clusters']))], palette=pal)

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
        <div>
            <span style='font-size: 12px'>@prediction</span>
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

    # output_notebook()
    output_file("data/umap_clusters.html",
                title="FAME results: UMAP clusters", mode='inline')
    # show(plot_figure)
    save(plot_figure)


def visualise_clusters_image(data, clusterer, labelIDs):
    print("[INFO] preparing visualisation clusters")
    # loop over the unique face integers
    for labelID in labelIDs:
        # find all indexes into the `data` array that belong to the current label ID, then randomly sample a maximum of 25 indexes from the set
        print("[INFO] preparing face ID: {}".format(labelID))
        idxs = np.where(clusterer.labels_ == labelID)[0]
        idxs = np.random.choice(idxs, size=min(25, len(idxs)), replace=False)

        # initialize the list of faces to include in the montage
        faces = []

        # loop over the sampled indexes
        for i in idxs:
            # load the input image and extract the face ROI
            try:
                image = cv2.imread(data.at[i, 'image_path'])
                (top, right, bottom, left) = data.at[i, 'face_location']
                face = image[top:bottom, left:right]

                # force resize the face ROI to 96x96 and then add it to the faces montage list
                face = cv2.resize(face, (96, 96))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

                faces.append(face)
                #print(data.at[i, 'image_path'])
            except:
                print("[ERROR] could not read image {}, skipping...".format(data.at[i, 'image_path']))

        # create a montage using 96x96 "tiles" with 5 rows and 5 columns
        count_rows = math.ceil(len(faces)/5)
        count_columns = len(faces) if len(faces) < 5 else 5
        montage = build_montages(faces, (96, 96), (count_columns, count_rows))[0]

        fig = plt.figure(figsize=(20, 30))
        # plt.imshow(montage)
        filename = 'data/clusters/cluster_' + str(labelID) + '.png'
        if labelID == -1:
            filename = 'data/clusters/not_clustered.png'
        plt.imsave(filename, montage)


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
                        if data.at[i, 'prediction'] == 'unknown':
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

    print("Unknown people before clustering:", (data.name == 'unknown').sum())
    print("Unknown people after clustering:",
          (data.prediction == 'unknown').sum())

    # print(len(data.loc[data['prediction'] == "unknown"]))
    # print(data['data.face_encoding'][0].shape)
    # data.to_pickle(
    #    "drive/My Drive/FaceRecognition/Results/Face-clustering-results.pickle")


def calculateNeighbors(data, encodings):
    print("[INFO] calculating neighbours")
    nbrs = NearestNeighbors(
        n_neighbors=20, algorithm='ball_tree').fit(encodings)
    distances, indices = nbrs.kneighbors(encodings)
    # print(indices, distances)
    '''
    for i in indices[9]:
    person = data.loc[i, 'name'] 
    cluster = data.loc[i, 'HDBSCAN_clusters']
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
    cluster = data.loc[i, 'HDBSCAN_clusters']
    # print(person, cluster)
    '''

    neighbors = []
    umapneighbors = []
    for i, row in data.iterrows():
        neighbors.append(indices[i].tolist())
        umapneighbors.append(knn_indices[i].tolist())

    data['neighbors'] = neighbors
    data['UMAP_neighbors'] = umapneighbors

    cluster = []
    for i, row in data.iterrows():
        c = data.at[i, 'HDBSCAN_clusters']

        if c != -1:
            lijst = data[data['HDBSCAN_clusters'] == c].index.tolist()
            cluster.append(lijst)
            #print(i, lijst, namen)
        else:
            lijst = []
            cluster.append(lijst)

    data['cluster_list'] = cluster


def write_data(data):
    data.to_pickle("data/pickle/face-clustering-results.pickle")
    data = data[['image_path', 'face_location', 'crop',
                 'HDBSCAN_clusters', 'cluster_list', 'prediction']]
    data.to_csv("data/predictions.csv", index=True, index_label='number')


# main

def cluster_and_predict():
    print("[INFO] Step 3: clustering and prediction")
    data = pickle.loads(open(
        "data/pickle/face_encoding.pickle", "rb").read())
    data = pd.DataFrame(data)
    predictions = cluster_faces(data)
    write_data(predictions)


cluster_and_predict()

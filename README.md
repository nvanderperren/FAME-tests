# FAME-tests

## Getting started

Install neceassary python packages.

```bash
pip3 install -r requirements.txt
```

Add portret and production folders in the `production_dirs` and `portret_dirs` variables in `workflow.py`.

Start the workflow

```bash
python3 workflow.py
```

## Results

You will find:

1. a csv with predictions (`predictions.csv`) in the `data/` folder
2. cropped faces in the `data/faces/` folder
3. a visualisation of the clusters in the `data/clusters/` folder
4. a UMAP visualisation (`UMAP_clusters.html`) in the `data/` folder

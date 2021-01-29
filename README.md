# FAME-tests

## Getting started

### Install

Clone this repository:

```bash
git clone https://github.com/nvanderperren/FAME-tests.git && cd FAME-tests
```

Install all neceassary python packages. __!IMPORTANT!__ use Python 3.8, some packages don't support Python 3.9.

```bash
pip3 install -r requirements.txt
```

### Prepare dataset (Kunstenpunt only)

The workflow needs a CSV with colums _image path_ (= absolute path of image) and _name_ (name of person on picture or unknown).
The script `preparations_KP.py` creates this CSV for the Kunstenpunt images.

1. mount the hard disk
2. add portret and production folders in the `production_dirs` and `portret_dirs` variables in `preparations_KP.py`
3. start the script: `python3 preparations_KP.py`

### Start the workflow

The workflow needs a CSV with columns _image path_ (= absolute path of image) and _name_ (name of person on picture or unknown).

You can adjust some parameters in `workflow.py`:

1. treshold: is now 0.7
2. csv_file: is now `data/filenames.csv`, which is created in previous step

Then, start the script:

```bash
python3 workflow.py
```

## Results

You will find:

1. a csv with predictions (`predictions.csv`) in the `data/` folder
2. cropped faces in the `data/faces/` folder
3. a visualisation of the clusters in the `data/clusters/` folder
4. a UMAP visualisation (`UMAP_clusters.html`) in the `data/` folder

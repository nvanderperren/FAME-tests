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
2. csv_file: is now `data/filenames.csv`, which is created in the first step

Then, start the script:

```bash
python3 workflow.py
```

### (Optional) Prepare data for labeling tool

(dit stuk moet nog beter uitgewerkt worden)

[EURECA project](https://tw06v072.ugent.be/eureca) is used to validate the results. To set up the labeling tool, some files need to be created. The `scripts/prepare_labeling.py` script creates these files.

Start the script with `python3 scripts/prepare_labeling.py`.

You'll see that a `data/labeling` folder is created in which you can find two CSV files.

## Results

You will find:

1. a csv with predictions (`predictions.csv`) in the `data/` folder
2. cropped faces in the `data/faces/` folder
3. a visualisation of the clusters in the `data/clusters/` folder
4. a UMAP visualisation (`UMAP_clusters.html`) in the `data/` folder
5. files needed for the labeling tool in the `data/labeling/` folder:
   1. `images.csv`: a list with face ID, path of cropped image, predictions and alike faces of each found face 
   2. `metadata.csv`: additional metadata per face (cropped image)

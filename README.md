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

### (Optional) Get extra metadata of path names (Kunstenpunt only)

The script needs:

* a CSV with columns _image path_ (= absolute path of image) and _name_ (name of person on picture or unknown);
* a CSV with the QID of the production company, QID of the production and the Kunstenpunt ID of the production. You can find this file `identifiers_KP.csv` in this repository.

You can adjust some parameters in `scripts/get_info_from_path.py`:

1. OUTPUT_FILENAME: the filename of the resulting csv file, now `kunstenpunt_data.csv`
2. IDENTIFIERS_CSV: the name of the csv with the identifiers, now `identifiers_KP.csv`
3. FILENAME_CSV: is now `data/filenames.csv`, which is created in first step

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

[EURECA project](https://tw06v072.ugent.be/eureca) is used to validate the results. To set up the labeling tool, some files need to be created. The `scripts/prepare_labeling.py` script creates these files.

Start the script with `python3 scripts/prepare_labeling.py`.

You'll see that a `data/labeling` folder is created in which you can find two CSV files.

## Results

You will find:

1. a csv with predictions (`predictions.csv`) in the `data/` folder
2. cropped faces in the `data/faces/` folder
3. a visualisation of the clusters in the `data/clusters/` folder
4. a UMAP visualisation (`UMAP_clusters.html`) in the `data/` folder
5. files needed for the labeling tool:
   1. `images.csv`: a list of path names, predictions and alike faces of each found person on a photo in the `data/preparation/` folder
   2. `metadata.csv`: additional metadata per face (cropped image), also in the `data/preparation/` folder

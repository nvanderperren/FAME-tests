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

You will find a csv with predictions (`predictions.csv`) in the `data/` folder and a visualisation of the clusters in the `data/clusters/` folder. (visualisations not implemented yet.)

# Scripts

Deze map bevat alle scripts die gebruikt worden door `workflow.py`.

1. `get_metadata.py`: maakt een lijst van alle beelden en plakt er een naam achter indien het om een portret gaat. Deze gegevens zullen later gebruikt worden bij het clusteren om een naam te plakken op een cluster.
2. `detect.py`: zoekt gezichten in foto's en bewaart de pixelcoördinaten van deze gezichten in het bestand `data/found-faces.csv`
3. `encode.py`: zet de gezichten (gecropte beelden) om in een vector. Deze vector wordt gebruikt in het volgend script om de gezichten te clusteren.
4. `cluster_and_predict.py`: clustert alle gezichten en plakt er een naam op indien er een portretfoto aanwezig is. Er worden in deze fase ook wat visualisaties aangemaakt en gecropte gezichten bewaard.
5. `prepare_labeling.py`: maakt alle bestanden aan die nodig zijn om de labeling tool op te zetten. De labeling tool wordt gebruikt om manueel de resultaten te valideren.

In de [preparation](preparation/README.md) map zitten nog enkele scripts die gebruikt kunnen worden om de gezichtsherkenningsworkflow voor te bereiden.

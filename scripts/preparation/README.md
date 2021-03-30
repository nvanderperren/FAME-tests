# FAME-tests

## Preparation scripts

Enkele scripts om te zorgen voor betere metadata en trainingsmateriaal.

### clean_photos.py

Dit script bekijkt of er 1 of meerdere mensen op een foto staan. Dit script is nog in testfase.

#### Gebruik

1. Zorg dat er een `portrets.csv` in de hoofdmap (FAME-tests) staat. In die CSV moeten minstens de padnamen staan van de foto's. Het werd voorlopig enkel getest met een CSV met 1 kolom waarin de padnamen staan, maar het zou ook met meerdere kolommen moeten werken.
2. start het script via `python3 scripts/preparation/clean_photos.py`.

Normaal zou het dan gewoon moeten uitvoeren. Duimen dat er geen fout in zit!

Je kan nog een aanpassing doen, nl. de treshold value aanpassen. Voorlopig staat dit op 0.7. Om dit aan te passen:

* open je het bestand `scripts/preparation/clean_photos.py`
* op lijn 25 zie je staan `treshold = 0.7`. Je kan die 0.7 vervangen in een hoger of lager cijfer.

Eerste test wees al uit dat 0.95 veel te hoog is. Het script ziet dan te weinig mensen als mensen, waardoor er te veel groepsfoto's in de portrettenmap staan. Wel worden de onduidelijke gezichten (mensen die wat fuzzy in de achtergrond staan) eruit gehaald. Moet nog beter onderzocht worden.

#### Resultaat

Het script maak mappen aan in de `data/` map:

* `test/empty`: hier komen foto's waarvan het script denkt dat er geen mens op staat
* `test/portrets`: hier komen dus de foto's waarvan het script denkt dat er 1 persoon op staat.
* `test/group`: de veronderstelde groepsfoto's.

Op al deze foto's zijn, in functie van testing, aangeduid waar het script denkt dat een mens staat + het waarschijnlijkheidspercentage.

Ook zal er een CSV verschijnen in de `data/` folder met als naam `cleanup_portrets.csv`. Hierin vind je een indexnummer (verwijzend naar de nummer van de foto's in de testmap), de originele bestandsnaam en het aantal gezichten dat het script denkt dat er op die foto's staan.

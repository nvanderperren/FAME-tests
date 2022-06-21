# Preparation scripts

Enkele scripts om te zorgen voor betere metadata en trainingsmateriaal.

## Opbouwen referentiesets

Scripts geschreven in het kader van het FAME-project voor het opbouwen van referetiesets

### download_from_wiki.py

Dit script download de afbeelding die aanwezig is in een wikidatarecord (_P18 has image_)

#### Vereisten

* [wikiget](https://github.com/clpo13/wikiget) is geïnstalleerd via `pip3 install --user wikiget`.

#### Gebruik

1. zorg dat je een CSV hebt met minstens de kolommen _QID_ en _image_. In de kolom QID staat het QID van de persoon, in _image_ de afbeelding.
2. start het script via `python3 scipts/preparation/download_from_wiki.py path_naar_csv_uit_stap_1 path_naar_output_map` 

#### Resultaat

In de gewenste outputmap zitten de gedownloadde afbeelding. De bestandsnaam van de afbeelding is steeds het QID.

### get_coureur_photos.py

Dit script werd gebruikt om de referentiesets voor wielrenners uit te breiden. Het stuurt drie shell scripts aan die foto's scrapen van _!!! de Wielersite !!!_, _Procyclingstats_ en _Wikimedia Commons_.

#### Vereisten

* een CSV met:
  * een kolom QID voor de QID van de wielrenner (verplicht);
  * een kolom _cyclingarchives_ met daarin het [Cycling Archives cyclist ID](https://www.wikidata.org/wiki/Property:P1409) van de wielrenner als je afbeeldingen van [!!! De Wielersite !!!](http://www.dewielersite.net/db2/wielersite/index.php) wil ophalen (optioneel);
  * een kolom _procyclingstats_ met daarin het [ProCyclingStats cyclist ID](https://www.wikidata.org/wiki/Property:P1663) van de wielerenner als je afbeeldingen van [ProCyclingStats](https://www.procyclingstats.com/) wil ophalen (optioneel);
  * een kolom _commons_ met daarin de naam van de [commons categorie](https://www.wikidata.org/wiki/Property:P373) voor de wielrenner waarvan je afbeeldingen wil ophalen (optioneel).
* de aanwezigheid van de scripts `commons_category_downloader.sh`, `dewielersite_image_downloader.sh` en `procyclingstats_image_downloader.sh` in dezelfde map als `get_coureur_photos.py`.

#### Gebruik

1. zorg dat je een CSV hebt met de kolommen zoals uitgelegd onder _Vereisten_.
2. start het script met `python3 get_coureur_photos.py path_van_csv path_van_output_folder` 
3. het script zal nu lijn voor lijn de CSV lezen. Als een van de kolommen van de websites aanwezig is en deze een identifier bevat, dan zal een script in werking gezet worden om de foto's van de wielrenner op de betreffende webste te scrapen. 

__Let op!__ het zijn redelijk inefficiënte scripts, waardoor het even kan duren. 

Hoe verloopt het under the hood? Via de identifier zal de webpagina van deze wielrenner gedownload worden. Vervolgens wordt gezocht naar de URL's van de afbeeldingen. Deze worden vervolgens één voor één gedownload en in de outputfolder gestopt. Daarna worden de gedownloade HTML-pagina's verwijderd.

#### Resultaat

In de outputfolder bevindt zich een map met het QID van de wielrenner. In deze map bevinden zich alle foto's die gescrapet werden van deze persoon.

## Kwaliteitscheck

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

### test_quality_photos.py

Dit script gaat na of de foto's geschikt zijn voor gezichtsherkenning

#### Gebruik

1. Zorg dat je een CSV hebt met alle padnamen van de foto's die je wil testen. In het script wordt er van uitgegaan dat deze CSV `filenames.csv` heet en zich in de hoofdmap van FAME bevindt. Indien gewenst kan je het pad van deze CSV wijzigen in het `test_quality_photos.py` bestand.

   * Ga hiervoor naar lijn 23 van `test_quality_photos.py`
   * Wijzig het pad achter `input_file: `. Momenteel staat hier `filenames.csv`

2. Start het script via `python3 scripts/preparation/test_quality_photos.py`.

#### Resultaat

Het script maakt de `preparation`-map aan waarin je `kwaliteit.csv` kan vinden. In deze CSV vind je per foto of het beeld gebruikt kan worden in de gezichtsherkenningworkflow.

### get_info_from_path.py (deprecated) 

Dit script haalde extra metadata uit de padnamen van de bestanden van Kunstenpunt. Sinds de cleaning van deze data is dit script niet meer nuttig.

#!/bin/bash
# author: Nastasia Vanderperren (meemoo)

ID=$1 # cycling archives ID of the coureur
OUTPUT_FOLDER=$2 # QID of the coureur
WIELERSITE=http://www.dewielersite.net/db2/wielersite/coureurfiche.php?coureurid=${ID}

echo $OUTPUT_FOLDER

echo "[INFO] Downloading coureur page: ${WIELERSITE}"
wget $WIELERSITE

echo "[INFO] Extracting image links"
WIELERSITE_LINKS=`grep beeldbank coureurfiche.php\?coureurid\=$ID | sed 's/^.*img src=//'| cut -d \" -f 2`
LINKS=${WIELERSITE_LINKS// /%20}
#echo $LINKS

echo "[INFO] Downloading images of ${WIELERSITE}"
wget -nc -w 1 -e robots=off -P ${OUTPUT_FOLDER} ${LINKS}


echo "[INFO] Cleaning up temp files"
rm coureurfiche*
echo "Done"

exit
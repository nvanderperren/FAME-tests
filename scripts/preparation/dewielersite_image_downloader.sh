#!/bin/bash
# author: Nastasia Vanderperren (meemoo)

ID=$1 # cycling archives ID of the coureur
QID=$2 # QID of the coureur
WIELERSITE=http://www.dewielersite.net/db2/wielersite/coureurfiche.php?coureurid=${ID}

echo "[INFO] Downloading coureur page"
wget $WIELERSITE

echo "[INFO] Extracting image links"
WIELERSITE_LINKS=`grep beeldbank coureurfiche.php\?coureurid\=$ID | sed 's/^.*img src=//'| cut -d \" -f 2`
LINKS=${WIELERSITE_LINKS// /%20}
#echo $LINKS

f [ ! -z $LINKS ]
then
    echo "[INFO] Downloading images"
    wget -nc -w 1 -e robots=off -P ${QID} ${LINKS}
else
    echo "[INFO] No images to download"
fi

echo "[INFO] Cleaning up temp files"
rm coureurfiche*
echo "Done"

exit
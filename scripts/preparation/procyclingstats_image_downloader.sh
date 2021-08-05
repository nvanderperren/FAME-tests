#!/bin/bash
# author: Nastasia Vanderperren (meemoo)

ID=$1 # cycling archives ID of the coureur
QID=$2 # QID of the coureur
WIELERSITE=https://www.procyclingstats.com/rider/${ID}/statistics

echo "[INFO]  Downloading coureur page"
wget $WIELERSITE

echo "[INFO] Extracting image links"
WIELERSITE_LINKS=`grep 'images/riders/' statistics | sed 's/^.*img src=//'| cut -d \" -f 2 | sed 's/^/https:\/\/www\.procyclingstats\.com\//'`
LINKS=${WIELERSITE_LINKS// /%20}
#echo $LINKS

if [ ! -z $LINKS ]
then
    echo "[INFO] Downloading images"
    wget -nc -w 1 -e robots=off -P ${QID} ${LINKS}
else
    echo "[INFO] No image links to extract"
fi

echo "[INFO] Cleaning up temp files"
rm statistics
echo "Done"

exit
ID=$1 # cycling archives ID of the coureur
QID=$2 # QID of the coureur
WIELERSITE=http://www.dewielersite.net/db2/wielersite/coureurfiche.php?coureurid=${ID}

echo "Downloading coureur page"
wget $WIELERSITE

echo "Extracting image links"
WIELERSITE_LINKS=`grep beeldbank coureurfiche.php\?coureurid\=$ID | sed 's/^.*a href=//'| sed 's/^.*img src=//'| cut -d " " -f 1 | sed 's/^.\(.*\).$/\1/'` 
echo ${WIELERSITE_LINKS}

echo "Downloading Images"
wget -nc -w 1 -e robots=off -P "${QID}" ${WIELERSITE_LINKS:1:-1}

echo "Cleaning up temp files"
rm coureurfiche*
echo "Done"

exit
ID=$1 # cycling archives ID of the coureur
QID=$2 # QID of the coureur
WIELERSITE=http://www.dewielersite.net/db2/wielersite/coureurfiche.php?coureurid=${ID}

echo "Downloading coureur page"
wget $WIELERSITE

echo "Extracting image links"
WIELERSITE_LINKS=`grep beeldbank coureurfiche.php\?coureurid\=$ID | sed 's/^.*a href=//'| sed 's/^.*img src=//'| cut -d \" -f 2`
LINKS=${WIELERSITE_LINKS// /%20}
#echo $LINKS

echo "Downloading Images"
wget -nc -w 1 -e robots=off -P ${QID} ${LINKS}

echo "Cleaning up temp files"
rm coureurfiche*
echo "Done"

exit
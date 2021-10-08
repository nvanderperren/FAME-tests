#!/bin/bash

CATEGORY=$1
FOLDER=$2
WIKI_URL="https://commons.wikimedia.org/wiki/Category:${CATEGORY}"

if [ "$WIKI_URL" == '' ]; then
	echo "The first argument is the main webpage"
	echo
	exit 1
fi

# Download Image pages
echo "Downloading Image Pages"
wget -r -l 1 -e robots=off -w 1 -nc $WIKI_URL

# Extract Image Links
echo "Extracting Image Links"
WIKI_LINKS=`grep fullImageLink commons.wikimedia.org/wiki/File\:* | sed 's/^.*a href="//'| sed 's/".*$//'`

echo "Downloading Images"
wget -nc -w 1 -e robots=off -P "${FOLDER}" $WIKI_LINKS


echo "Cleaning up temp files"
rm -rf commons.wikimedia.org/
echo "Done"

exit

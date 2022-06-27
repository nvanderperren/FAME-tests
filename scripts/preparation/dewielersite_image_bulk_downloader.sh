#!/bin/bash
# author: Nastasia Vanderperren (meemoo)

CSV=$1 # input csv with columns qid,name,cyclingarchives_id; header is required
OUTPUT_FOLDER=$2 # folder where you want all images to be stored

tail -n +2 ${CSV} | \
while IFS="," read -r qid name cyclingarchives_id
do

    if [[ -n $cyclingarchives_id ]]; then

        echo "[INFO] Searching for images of ${name}"

        folder="${OUTPUT_FOLDER}/${qid}"
        WIELERSITE="http://www.dewielersite.net/db2/wielersite/coureurfiche.php?coureurid=${cyclingarchives_id}"

        echo "[INFO] Downloading coureur page: ${WIELERSITE}"
        wget -q $WIELERSITE

        echo "[INFO] Extracting image links"
        WIELERSITE_LINKS=`grep beeldbank coureurfiche.php\?coureurid\=${cyclingarchives_id} | sed 's/^.*img src=//'| cut -d \" -f 2`
        LINKS=${WIELERSITE_LINKS// /%20}
        #echo $LINKS

        if [[ -n $LINKS ]]; then
            echo "[INFO] Downloading images of ${WIELERSITE}"
            wget -q -nc -w 1 -e robots=off -P ${folder} ${LINKS}
            echo "[INFO] Files saved in ${folder}"
        else
            echo "[INFO] Coureur page of $name has no images"
        fi

        echo "[INFO] Cleaning up temp files"
        rm coureurfiche*
        echo -e "Done\n"

    fi

done


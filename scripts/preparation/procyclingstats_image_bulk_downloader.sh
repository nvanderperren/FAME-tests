#!/bin/bash
# author: Nastasia Vanderperren (meemoo)

CSV=$1 # input csv with columns qid,name,procyclingstats_id; header is required
OUTPUT_FOLDER=$2 # folder where you want all images to be stored

tail -n +2 ${CSV} | \
while IFS="," read -r qid name procycling_id
do
    
    if [[ -n $procycling_id ]]; then
        
        echo "[INFO] Searching for images of $name"
        folder="${OUTPUT_FOLDER}/$qid"
        WIELERSITE="https://www.procyclingstats.com/rider/${procycling_id}/statistics"
        
        echo "[INFO] Downloading coureur page: ${WIELERSITE}"
        wget -q $WIELERSITE
        
        echo "[INFO] Extracting image links"
        WIELERSITE_LINKS=`grep 'images/riders/' statistics | sed 's/^.*img src=//'| cut -d \" -f 2 | sed 's/^/https:\/\/www\.procyclingstats\.com\//'`
        LINKS=${WIELERSITE_LINKS// /%20}
        
        if [[ -n $LINKS ]]
        then
            echo "[INFO] Downloading images of ${WIELERSITE}"
            wget -q -nc -w 1 -e robots=off -P ${folder} ${LINKS}
            echo "[INFO] Files saved in ${folder}"
        else
            echo "[INFO] Coureur page of $name has no images"
        fi
        
        echo "[INFO] Cleaning up temp files"
        rm statistics
        echo -e "Done\n"
        
    fi
    
done
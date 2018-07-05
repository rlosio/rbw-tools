#!/bin/bash
EVENTS_FILE=../backup/races-$(date +"%Y%m%d-%H%M%S").json
curl "https://api.trailburning.com/v2/search?limit=10000" > $EVENTS_FILE
minimumsize=100000
actualsize=$(wc -c <"$EVENTS_FILE")
if [ $actualsize -le $minimumsize ]; then
    echo WARNING: size $actualsize is under $minimumsize bytes, backup is missing
fi


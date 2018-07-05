#!/bin/bash
EVENTS_FILE=../origin/races.json
rm  -f $EVENTS_FILE
curl "https://api.trailburning.com/v2/raceevents" > $EVENTS_FILE


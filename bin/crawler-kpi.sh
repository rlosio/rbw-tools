#!/bin/bash

cd /home/ubuntu/racebase/bin
PATH=$PATH:/usr/local/bin
export PATH
export HOME=/home/ubuntu

EVENTS_FILE=../origin/stats/races.json
EVENTS_FILE_TRAIL=../origin/stats/races-trail.json
EVENTS_FILE_ROAD=../origin/stats/races-road.json
DUPLICATE_EVENT_FILE=../origin/stats/duplicate-events.txt
DUPLICATE_RACE_FILE=../origin/stats/duplicate-races.txt
EVENTS_MESSAGE=../origin/stats/message.json
EVENTS_MESSAGE_TXT=../origin/stats/message.txt
USERS_FILE=../origin/stats/users.json

rm $DUPLICATE_EVENT_FILE
rm $DUPLICATE_RACE_FILE
rm $EVENTS_FILE
rm $EVENTS_FILE_TRAIL
rm $EVENTS_FILE_ROAD
rm $EVENTS_MESSAGE
rm $EVENTS_MESSAGE_TXT
rm $USERS_FILE

curl "https://api.trailburning.com/v2/search?limit=10000&type=road_run" > $EVENTS_FILE_ROAD
curl "https://api.trailburning.com/v2/search?limit=10000&type=trail_run" > $EVENTS_FILE_TRAIL
# curl "https://api.trailburning.com/v2/user/latest?limit=10000" > $USERS_FILE
curl "https://api.trailburning.com/v2/summary" > $USERS_FILE
 
jq -s '.[0] as $o1 | .[1] as $o2 | ($o1 + $o2) | .body.raceevents = ($o1.body.raceevents + $o2.body.raceevents)' $EVENTS_FILE_TRAIL $EVENTS_FILE_ROAD > $EVENTS_FILE


# curl "https://api.trailburning.com/v2/raceevents" > $EVENTS_FILE

minimumsize=100000
actualsize=$(wc -c <"$EVENTS_FILE")
if [ $actualsize -le $minimumsize ]; then
    echo size $actualsize is under $minimumsize bytes
    echo quitting... without KPI
    exit
fi

cat $EVENTS_FILE | jq .body.raceevents[].name | sort | uniq -d > $DUPLICATE_EVENT_FILE
cat $EVENTS_FILE | jq '.body.raceevents[].races[] | .name + (.date|tostring) + (.distance|tostring)' | sort | uniq -d > $DUPLICATE_RACE_FILE
TODAY_DATE=$(date +"%Y-%m-%d")
DUPLICATE_NAME_NUM=$(cat $DUPLICATE_EVENT_FILE | wc -l)
EVENT_NUM=$(cat $USERS_FILE | jq .body.summary.race_event_count)
EVENT_TRAIL_NUM=$(cat $EVENTS_FILE | jq .body.raceevents[].type | grep 'trail_run' | wc -l)
EVENT_ROAD_NUM=$(cat $EVENTS_FILE | jq .body.raceevents[].type | grep 'road_run' | wc -l)
RACE_NUM=$(cat $EVENTS_FILE | jq .body.raceevents[].races[].date | wc -l)
RACE_NUM_FUTURE=$(curl "https://api.trailburning.com/v2/search?dateFrom=2017-06-29" | jq .meta.count)
DUPLICATE_RACE_NUM=$(cat $DUPLICATE_RACE_FILE | wc -l)
# NUM_USERS=$(cat $USERS_FILE | jq .body.user[].id | wc -l)
NUM_USERS=$(cat $USERS_FILE | jq .body.summary.user_count)
EMAIL_NUM=$(cat $EVENTS_FILE | jq .body.raceevents[].email | sort | uniq | wc -l)
COUNTRY_NUM=$(cat $USERS_FILE | jq .body.summary.country_count)
MEDIA_NUM=$(cat $EVENTS_FILE | jq .body.raceevents[] | grep sharePath | wc -l) 

PERCENTAGE_FUTURE=$(awk "BEGIN { pc=100*(${RACE_NUM_FUTURE})/${EVENT_NUM}; i=int(pc); print (pc-i<0.5)?i:i+1 }")
echo '{"Subject": {"Data": "RaceBase database status","Charset": "UTF8"},"Body": {"Text": {"Data":"' >> $EVENTS_MESSAGE
echo "" >> $EVENTS_MESSAGE
echo "RaceBase database status $TODAY_DATE" >> $EVENTS_MESSAGE
echo "" >> $EVENTS_MESSAGE
echo "Number of users:  $NUM_USERS" >> $EVENTS_MESSAGE 
echo "Number of events: $EVENT_NUM" >> $EVENTS_MESSAGE
echo "Future events: ${RACE_NUM_FUTURE} ( $PERCENTAGE_FUTURE % )" >> $EVENTS_MESSAGE
echo "Number of events type trail_run: $EVENT_TRAIL_NUM" >> $EVENTS_MESSAGE
# echo "Number of events type road_run: $EVENT_ROAD_NUM" >> $EVENTS_MESSAGE
echo "Number of countries: $COUNTRY_NUM" >> $EVENTS_MESSAGE
# echo "Number of races: $RACE_NUM" >> $EVENTS_MESSAGE
# echo "Number of races in the future: $RACE_NUM_FUTURE" >> $EVENTS_MESSAGE
echo "Number of unique email addresses: $EMAIL_NUM" >> $EVENTS_MESSAGE
# echo "Number of unique email addresses: NA"
echo "Number of pictures: $MEDIA_NUM" >> $EVENTS_MESSAGE
# echo "Number of pictures: NA"
# echo "Number of duplicate events: $DUPLICATE_NAME_NUM" >> $EVENTS_MESSAGE
# echo "Number of duplicate races/distances: $DUPLICATE_RACE_NUM" >> $EVENTS_MESSAGE
echo "" >> $EVENTS_MESSAGE
echo '","Charset": "UTF8"}}}' >> $EVENTS_MESSAGE

# cat $EVENTS_MESSAGE
cat $EVENTS_MESSAGE | tr '\r' ' ' |  tr '\n' ' ' | sed 's/ \{3,\}/ /g' | sed 's/   / /g' > $EVENTS_MESSAGE_TXT
aws ses send-email --debug --to <email-here> --from <email-here> --message file://$EVENTS_MESSAGE_TXT


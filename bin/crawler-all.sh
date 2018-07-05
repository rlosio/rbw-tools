#!/bin/bash

cd /home/ubuntu/racebase/bin
PATH=$PATH:/usr/local/bin
export PATH

TODAY_DATE=$(date +"%Y-%m-%d")
echo ""
echo "RaceBase database update $TODAY_DATE"
echo ""
echo "Start backup current status..."
./backup-crawler.sh
echo "Backup completed"
echo ""
echo "Start crawling main sites incrementally"
cd ../racebasetest/spiders/
scrapy crawl trailrunnerincremental -o ../output/trailrunner-$TODAY_DATE.json > ../../output/trailrunner-$TODAY_DATE.log
scrapy crawl ahotuincremental -o ../output/ahout-$TODAY_DATE.json > ../../output/ahotu-$TODAY_DATE.log
echo ""
echo "Crowling completed"
echo ""
echo "Fixing type for road races with name trail"
scrapy crawl fixtrailtag > ../output/fixtrailtag-$TODAY_DATE.log
echo ""
echo "Cleanup duplicates started"
scrapy crawl dupremover -o ../output/dupremover-$TODAY_DATE.json > ../output/dupremover-$TODAY_DATE.log
echo ""
echo "Cleanup duplucates completed"
echo ""
echo "Cleanup races with event both in the past and the future started"
scrapy crawl cleanup -o ../output/cleanup-$TODAY_DATE.json > ../output/cleanup-$TODAY_DATE.log
scrapy crawl cleanupurl -o ../output/cleanupurl-$TODAY_DATE.json > ../output/cleanupurl-$TODAY_DATE.log
echo ""
echo "Starting blacklist task"
scrapy crawl blacklist -o ../output/blacklist-$TODAY_DATE.json > ../output/blacklist-$TODAY_DATE.log
echo "Ending blacklist task"
echo ""
echo "Cleanup races completed"
cd ../../bin/
echo ""
# echo "Time for KPI..."
# ./crawler-kpi.sh
# echo ""
echo "Update for $TODAY_DATE compeleted"
echo ""


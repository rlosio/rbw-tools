#!/bin/bash

cd /home/ubuntu/racebase/bin
PATH=$PATH:/usr/local/bin
export PATH
export HOME=/home/ubuntu

aws ses send-email --to rlosio@gmail.com --from rlosio@gmail.com --region eu-west-1 --message "Subject={Data='RaceBase database status hello',Charset='UTF8'},Body={Text={Data='renato',Charset='UTF8'}}"


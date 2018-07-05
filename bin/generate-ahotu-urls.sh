#!/bin/bash
for ((a=1; a <= $1 ; a++))
do
   echo "\"http://marathons.ahotu.com/calendar/$2?page=$a&sort_by=date_descending\","
done

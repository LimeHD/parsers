#!/bin/bash

echo "Create directory for temporary binary files"

mkdir -p $(pwd)/tmp/cron

echo "" > $(pwd)/tmp/cron/crontab

for filename in $(pwd)/*.py; do
  file=$(basename $filename)
  FILE="${file%%.*}"
  
  echo "Create cron command for $FILE output to $(pwd)/tmp/bin/cron"
  
  echo "*/15 * * * *   cd ~/epg_parsers/current; ./bin/tvparser_$FILE >> /home/master/epg_parsers/shared/log/tvparser_$FILE.log 2>&1" >> $(pwd)/tmp/cron/crontab
done
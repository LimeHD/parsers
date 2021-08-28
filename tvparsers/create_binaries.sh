#!/bin/bash

echo "Create directory for temporary binary files"

mkdir -p $(pwd)/tmp/bin


for filename in $(pwd)/*.py; do
  file=$(basename $filename)
  FILE="${file%%.*}"
  
  echo "Create binaty for $FILE output to $(pwd)/tmp/bin/tvparser_$FILE"
  
  if [ -e $(pwd)/tmp/bin/tvparser_$FILE ]; then
	echo "File /tvparser_$FILE already exists! Skip.."
  else
	echo "docker run -v ~/epg_parsers/shared/output:/out --rm -i tv_parsers:latest $FILE.py --output /out/$FILE.csv" > $(pwd)/tmp/bin/tvparser_$FILE
  fi
done
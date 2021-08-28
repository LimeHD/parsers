#!/bin/bash

echo "Create directory for temporary output files"

mkdir -p $(pwd)/tmp/all

echo "Create image (tv_parsers:latest) if not exist"

docker build -t tv_parsers:latest .

for filename in $(pwd)/*.py; do
  file=$(basename $filename)

  echo "Execute $file output to ./tmp/all/$file.csv"

  docker run -v $(pwd)/tmp/all:/out --rm -it tv_parsers $file --output /out/$file.csv
done
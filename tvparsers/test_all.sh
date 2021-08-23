#!/bin/bash

mkdir -p $(pwd)/tmp/all

for filename in $(pwd)/*.py; do
  file=$(basename $filename)

  echo "Execute $file output to ./tmp/all/$file.csv"

  python3 $file --output $(pwd)/tmp/all/$file.csv

  #sql=$(<$filename)
  #docker run --rm --network="clickhouse-net" --link clickhouse-$1:clickhouse-server yandex/clickhouse-client -m --host clickhouse-server --query="$sql"
done
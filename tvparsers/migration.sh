#!/bin/bash

query="insert into epg_sources (title, comment, created_at, updated_at, is_enabled, file, file_modified_at, parser_type) values"

for filename in $(pwd)/*.py; do
  file=$(basename $filename)
  FILE="${file%%.*}"
   
  query+=" ('$FILE', '$FILE.csv', '2021-08-28 00:01:40.000000', '2021-08-28 00:01:40.000000', 1, '$FILE.csv', '2021-08-28 00:05:00', 'common'),"
done

query=${query::-1}
query+=";"

echo $query
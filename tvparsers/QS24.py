#!/usr/bin/env python3
import smbclient
from datetime import datetime, date, time, timedelta, tzinfo
import xlrd
import csv
from pytz import timezone
from itertools import zip_longest

import argparse

CHANNEL = "QS24"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/11194/photo_2021-07-06_16.jpeg"
berlin = timezone('Europe/Berlin')

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')


def main():
    (year, week, _) = datetime.now().isocalendar()

    smbclient.ClientConfig(username='user1', password='5f217c95')
    args = parser.parse_args()

    with smbclient.open_file('\\194.35.48.33\home\QS24\{0}_{1}.xls'.format(year, week), mode="rb") as f:
        wb = xlrd.open_workbook("myfile.xls", use_mmap=False, file_contents=f.read())

    ws = wb.sheet_by_index(0)
    data = []
    for row in ws.get_rows():
        if row[0].ctype != 3:
            continue

        start_date = xlrd.xldate.xldate_as_datetime(row[0].value, 0).date()
        start_time = xlrd.xldate.xldate_as_datetime(row[1].value, 0).time()
        data.append({
            "start_at": datetime.combine(start_date, start_time),
            "title": row[2].value,
            "description": row[3].value
        })

    template = {
        'channel': CHANNEL,
        'logo': LOGO_URL,
        'archive_available': ARCHIVE_AVAILABLE,
        'available': AVAILABLE
    }

    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for i, next_i in zip_longest(data, data[1:]):
            if next_i:
                i['end_at'] = next_i["start_at"]
            else:
                i['end_at'] = (i['start_at'] + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

            for k in ("start_at", "end_at"):
                i[k] = berlin.localize(i[k]).isoformat()

            writer.writerow({**template, **i})

if __name__ == '__main__':
    main()

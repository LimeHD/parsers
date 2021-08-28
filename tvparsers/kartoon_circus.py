#!/usr/bin/env python3
import csv
from datetime import datetime, timedelta, tzinfo
import io
import argparse
import itertools

import requests
from bs4 import BeautifulSoup

class EST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours = -5)

    def tzname(self, dt):
        return "EST"

    def dst(self, dt):
        return timedelta(0)

URL = "https://morcaman.com/kartoon-fun-time-schedule/"
CHANNEL = "Kartoon Circus"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/10681/IMG_5647.JPG"
headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')

def main():
    args = parser.parse_args()
    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['start_at', 'end_at', 'channel', 'title', 'logo', 'description', 'archive_available', 'available'])
        r = requests.get(URL, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        rows = [[j.string.strip() for j in i.find_all("td")] for i in soup.table.tbody.find_all("tr")[1:]]
        for tds, next_row in itertools.zip_longest(rows, rows[1:]):
            start_time = datetime.strptime("{} {}".format(tds[1], tds[2]), "%d/%m/%Y %H:%M:%S").replace(tzinfo=EST())
            if next_row:
                end_time = datetime.strptime("{} {}".format(tds[1], next_row[2]), "%d/%m/%Y %H:%M:%S").replace(tzinfo=EST())
            else:
                end_time = datetime.strptime("{} 23:59:00".format(tds[1]), "%d/%m/%Y %H:%M:%S").replace(tzinfo=EST())

            writer.writerow({
                'start_at': start_time.isoformat(),
                'end_at': end_time.isoformat(),
                'channel': CHANNEL,
                'title': tds[0],
                'logo': LOGO_URL,
                'description': "",
                'archive_available': ARCHIVE_AVAILABLE,
                'available': AVAILABLE
            })

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import requests
import csv
from datetime import datetime, timedelta
import argparse
from lxml import etree

URL = "https://30a-tv.com/feeds/ceftech/beachshow.xml"
CHANNEL = "The Beach Show (eng)"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/11033/BeachShow.jpg"

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')

template = {
    'channel': CHANNEL,
    'logo': LOGO_URL,
    'archive_available': ARCHIVE_AVAILABLE,
    'available': AVAILABLE
}

time_format = "%m/%d/%Y %H:%M:%S.%f%z"

def main():
    args = parser.parse_args()
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        r = requests.get(URL)
        xml = etree.XML(r.content)
        for i in xml.xpath('/tv/programme'):
            d = {
                'start_at': datetime.strptime(i.attrib["start"], time_format).isoformat(),
                'end_at': datetime.strptime(i.attrib["stop"], time_format).isoformat(),
                'title': i.xpath("title/text()")[0],
                'description': i.xpath("desc/text()")[0],
            }
            writer.writerow({**template, **d})

if __name__ == '__main__':
    main()

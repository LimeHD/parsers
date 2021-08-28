#!/usr/bin/env python3
import requests
import csv
from datetime import datetime, timedelta
import argparse
import re
from lxml import etree
from pytz import timezone

URL = "https://www.weltderwunder.de/epg_v2.xml?date={}&days=7".format(datetime.now().strftime("%Y%m%d"))
CHANNEL = "Welt der Wunder"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/11117/thumb_photo_2021-06-21_10-16-43.jpg"
berlin = timezone('Europe/Berlin')

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')

def main():
    args = parser.parse_args()
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        r = requests.get(URL)
        xml = etree.XML(r.content)
        for event in xml.xpath('/epg/event'):
            date = event.attrib["datum"]
            time = event.attrib["sendezeit"]
            duration = event.xpath("sendung/dauer/text()")[0]
            (h,m,s) = map(int, re.match('(\d{2})(\d{2})(\d{2})', duration).groups())
            seconds = (h * 60 + m) * 60 + s
            start_time = datetime.strptime("{} {}".format(date, time), "%Y%m%d %H%M%S")
            end_time = start_time + timedelta(seconds = seconds)

            description = event.xpath("sendung/programmtext/text()")
            writer.writerow({
                'start_at': start_time.astimezone(berlin).isoformat(),
                'end_at': end_time.astimezone(berlin).isoformat(),
                'channel': CHANNEL,
                'title': event.xpath("sendung/titel/text()")[0],
                'logo': LOGO_URL,
                'description': description[0] if description else "",
                'archive_available': ARCHIVE_AVAILABLE,
                'available': AVAILABLE
            })


if __name__ == '__main__':
    main()

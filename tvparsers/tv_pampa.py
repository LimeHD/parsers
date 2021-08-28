#!/usr/bin/env python3
from datetime import datetime, date, time, timedelta, tzinfo
import csv
import requests
from pytz import timezone

import lxml.html

import argparse

URL = "https://www.tvmap.com.br/TV-Pampa"
CHANNEL = "TV PAMPA"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/10977/thumb_photo_2021-06-09_07-41-12.jpg"

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')

sao_paulo = timezone('America/Sao_Paulo')

template = {
    'channel': CHANNEL,
    'logo': LOGO_URL,
    'description': "",
    'archive_available': ARCHIVE_AVAILABLE,
    'available': AVAILABLE
}

def main():
    today = datetime.now().astimezone(sao_paulo).date()
    args = parser.parse_args()
    r = requests.get(URL)
    html = lxml.html.fromstring(r.content)

    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        data = []
        for i in html.xpath('//ul[@id="timelineul"]/li'):
            title = i.xpath('div[@class="timelineheader"]/a/b/text()')[0]
            t = i.xpath('div[@class="hourbox"]/p/span/text()')[0]
            t = datetime.strptime(t, "%H:%M h").time()
            data.append((t, title))

        data.append((time(hour = 23, minute = 59), ""))

        for (start_time, title), (end_time, _) in zip(data, data[1:]):
            writer.writerow({**template, **{
                "start_at": sao_paulo.localize(datetime.combine(today, start_time)).isoformat(),
                "end_at": sao_paulo.localize(datetime.combine(today, end_time)).isoformat(),
                "title": title
            }})

if __name__ == '__main__':
    main()

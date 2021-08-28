#!/usr/bin/env python3
from datetime import datetime, date, time, timedelta, tzinfo
import csv
import requests
from pytz import timezone

import lxml.html

import argparse

URL = "http://www.tvaracati.com.br/programacao"
CHANNEL = "TV Aracati"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/11299/thumb_TV_Arcati.png"

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
    (year, week, _) = datetime.now().isocalendar()
    args = parser.parse_args()
    r = requests.get(URL)
    html = lxml.html.fromstring(r.content)

    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for day in range(1,8):
            data = []
            d = date.fromisocalendar(year, week, day)
            i = html.xpath('//section[@id="content{}"]'.format(day))[0]
            for j in i.xpath('div[@class="layprog"]'):
                title = j.xpath('div[@class="layprog3"]/span[@class="fonte1"]/text()')[0].strip()
                t = j.xpath('div/h1/text()')[-1]
                t = datetime.strptime(t, "%H:%M").time()
                data.append((t, title))

            data.append((time(hour = 23, minute = 59), ""))

            for (start_time, title), (end_time, _) in zip(data, data[1:]):
                writer.writerow({**template, **{
                    "start_at": sao_paulo.localize(datetime.combine(d, start_time)).isoformat(),
                    "end_at": sao_paulo.localize(datetime.combine(d, end_time)).isoformat(),
                    "title": title
                }})

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
from datetime import datetime, date, time, timedelta, tzinfo
import csv
import requests
from pytz import timezone

import lxml.html

import argparse

URL = "http://canalyeeah.com.br/programacao/"
CHANNEL = "Yeeaah TV"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/10795/http-__canalyeeah.jpeg"

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')

sao_paulo = timezone('America/Sao_Paulo')

weekdays = ["SEGUNDA","TERÇA","QUARTA","QUINTA","SEXTA","SÁBADO","DOMINGO"]

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
    day_map = {}

    for title in html.xpath('//div[contains(@class, "elementor-tab-title")]'):
        day = title.xpath("a/text()")

        if not day:
            break

        day_map[day[0]] = title.attrib["aria-controls"]

    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for day, day_name in enumerate(weekdays, 1):
            d = date.fromisocalendar(year, week, day)
            id = day_map[day_name]
            data = []
            for i in html.xpath('//div[@id="{}"]/p'.format(id)):
                s = i.text_content().replace('\xa0', ' ')
                t, _, title = s.partition(" – ")
                t = datetime.strptime(t, "%Hh%M").time()
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

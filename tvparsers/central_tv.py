#!/usr/bin/env python3
from datetime import datetime, date, time, timedelta, tzinfo
import csv
import requests
import codecs
from pytz import timezone
import re

from pprint import pprint
import argparse

URL = "https://www.redecentraltv.com.br/grade-de-programacao"
CHANNEL = "Central TV"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/11264/Central_TV.jpeg"

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')

sao_paulo = timezone('America/Sao_Paulo')

re_time = re.compile('\d{2}:\d{2}')

template = {
    'channel': CHANNEL,
    'logo': LOGO_URL,
    'description': "",
    'archive_available': ARCHIVE_AVAILABLE,
    'available': AVAILABLE
}

csv_urls = [
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRIiF_bi_-VyWeS8ND6YtPk8CPLoujk4KGNsJ-nn5KvXnl1OJ_2FVEwQ9PVG1SI49ncmsb_yEzjASDU/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkT1uI_OywNwi0EOMb3KsWAMVWKxB_x9v_cM7Ojfw2QnNVWKtxJ0dZB4M-Gw8hkZ7vldqBgu_VT1Ip/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpqKhx54FOd41uAWwel28CpIf679TlNbltZGipqalLdwRCaqK4uWdY10eIVYxcijFk5QfuYEihPE54/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQWaH315x4xT3T0V-CjRuRdkeAKmM91i3xIGUhlfAVoeICSKx5jkpP8qUFtAZWPpl4-tXKSQmrxN1sd/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTK9jyUUHZZjY1_5FtBYanwrnNP175X8_14oErBZhlqCghaQfFWwVFYrzzmmviQnKM_Xo3GTSCV79tK/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQoNni10Oe2octQ9Ev2UO4tAuC8CmTqwa2clQ97CRmQQGD5Jndf59CyWySet3K6S15qw_2O3XeAdxBy/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTk_1H1Y1qZ026z43n_Gt1fsuMtuXlHVL4UrwbJFsUYvHZfpL21bVZQrUqmklm5kPFGGRASrbLjcr9R/pub?output=csv"
]

def main():
    (year, week, _) = datetime.now().isocalendar()
    args = parser.parse_args()
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for day, url in enumerate(csv_urls, 1):
            d = date.fromisocalendar(year, week, day)
            r = requests.get(url, stream=True)
            reader = csv.reader(codecs.iterdecode(r.raw, 'utf-8'))
            for row in reader:
                if not re_time.match(row[3]):
                    continue

                t = datetime.strptime(row[2], "%H:%M").time()
                dur = datetime.strptime(row[3], "%H:%M").time()

                start_time = sao_paulo.localize(datetime.combine(d, t))
                end_time = start_time + timedelta(hours=dur.hour, minutes=dur.minute)

                writer.writerow({**template, **{
                    "start_at": start_time.isoformat(),
                    "end_at": end_time.isoformat(),
                    "title": row[4]
                }})

if __name__ == '__main__':
    main()

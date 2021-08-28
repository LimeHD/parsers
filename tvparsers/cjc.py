#!/usr/bin/env python3
import requests
import csv
from datetime import datetime, timedelta
import argparse

URL = "https://portal2.teleosmedia.com/epg/?channel_id=cjc&client_id=cje&days=7"
CHANNEL = "CJC"
ARCHIVE_AVAILABLE = 0
AVAILABLE = 1
LOGO_URL = "https://assets.iptv2022.com/uploads/channel/11061/image.jpg"

parser = argparse.ArgumentParser(description=f'Get program for {CHANNEL}')
parser.add_argument('--output', default="out.csv", help='output csv name')

def main():
    args = parser.parse_args()
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['start_at', 'end_at', 'channel', 'title', 'logo', 'description', "archive_available", "available"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for week in requests.get(URL).json()["items"]:
            if not week:
                continue
            for i in week:
                i['end_at'] = (datetime.strptime(i["start_at"], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(seconds=i["adjusted_duration"])).isoformat(timespec='minutes') + "Z"
                i['channel'] = CHANNEL
                i['logo'] = LOGO_URL
                i['archive_available'] = ARCHIVE_AVAILABLE
                i['available'] = AVAILABLE
                for f in ('guid', 'duration', 'adjusted_duration', 'type', 'rating'):
                    del i[f]
                writer.writerow(i)

if __name__ == '__main__':
    main()

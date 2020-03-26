import csv
import json
import datetime
from pathlib import Path
# import requests
from os import listdir
from os.path import isfile, join


INPUT_DIR = Path("./dist")
FILE_PATH = join(INPUT_DIR, "chiffres-cles.json")

with open(FILE_PATH, 'r', encoding='utf8') as infile:
    all_data = json.load(infile)

new_data = []
today = datetime.date.today()
delta = today - datetime.timedelta(days=30)

for entry in all_data:
    date = datetime.datetime.strptime(entry['date'], '%Y-%m-%d').date()
    if delta <= date:
        # print (date)
        if entry['source']:
            del entry['source']
        new_data.append(entry)


# TODO should override FILE_PATH
# print (new_data)
with open("test.json", 'w', encoding='utf8') as outfile:
    json.dump(new_data, outfile, ensure_ascii=False)
import csv
import json
import datetime
from pathlib import Path
# import requests
from os import listdir
from os.path import isfile, join
from operator import itemgetter


INPUT_DIR = Path("./dist")
INPUT_FILE_PATH = join(str(INPUT_DIR), "chiffres-cles.json")
OUTPUT_FILE_PATH = join(str(INPUT_DIR), "chiffres-cles-filtered-consolidated.json")
DAYS_ROLLING = 30

with open(INPUT_FILE_PATH, 'r', encoding='utf8') as infile:
    all_data = json.load(infile)

today = datetime.date.today()
delta = today - datetime.timedelta(days=DAYS_ROLLING)

new_dict = {}
for entry in all_data:
    date = datetime.datetime.strptime(entry['date'], '%Y-%m-%d').date()
    # if delta > date: # mustn't be use here since we use history to fill missing values
    #     continue

    key_ = (date, entry['code'], entry['nom'])
    if key_ not in new_dict:
        new_dict[key_] = {}

    for type_of_entry in ['casConfirmes', 'deces', 'hospitalises', 'reanimation', 'gueris']:
        if type_of_entry in entry and entry[type_of_entry]:
            if type_of_entry not in new_dict[key_]:
                new_dict[key_][type_of_entry] = entry[type_of_entry]
            elif entry[type_of_entry] > new_dict[key_][type_of_entry]:
                new_dict[key_][type_of_entry] = entry[type_of_entry]

                
        if type_of_entry not in new_dict[key_]:
            for k in sorted(new_dict.keys(), key=itemgetter(0,1,2), reverse=True):
                code = k[1]
                nom = k[2]
                v = new_dict[k]
                if code == entry['code'] and nom == entry['nom'] and type_of_entry in v:
                    new_dict[key_][type_of_entry] = v[type_of_entry]
                    break

    print (date)


# for k, v in new_dict.items():
#     print (k, v)


new_data = []
for k in sorted(new_dict.keys(), key=itemgetter(0,1,2)):
    date = k[0]
    code = k[1]
    nom = k[2]
    v = new_dict[k]
    # print (date, code, nom, v)

    if delta > date:
        continue

    values = {
        'date': date.strftime("%Y-%m-%d"),
        'code': code,
        'nom': nom,
    }
    values.update(v)

    new_data.append(values)

# print (new_data)
print (OUTPUT_FILE_PATH)
with open(OUTPUT_FILE_PATH, 'w', encoding='utf8') as outfile:
    json.dump(new_data, outfile, ensure_ascii=False)

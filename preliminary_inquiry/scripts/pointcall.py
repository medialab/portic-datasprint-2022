'''
    File name: poincall.py
    Author: Guillaume Brioudes
    Date created: 2022-01-31
    Date last modified: 2022-01-31
    Python Version: 3.10.1
    Description: Get pointcalls data with Dunkerque as pointcall
'''

import csv

fields = [
    'year',
    'homeport',
    'homeport_state_1789_fr',
    'flag',
    'tonnage',
    'tonnage_class',
    'commodity_standardized_fr',
    'pointcall',
    'ferme_bureau',
    'ferme_direction',
    'pointcall_province',
    'pointcall_admiralty',
    'pointcall_action'
]

rows = []

CSV_FILE_OUTPUT = '../src/static/data/pointcalls.csv'

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_pointcalls_' + year + '.csv'

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row_original in reader:
            # if row_original['pointcall'] != 'Dunkerque':
            #     continue

            row = dict.fromkeys(
                fields,
                '' # initial value for all fields
            )
            for meta in row.keys():
                if meta == 'year':
                    row[meta] = year
                    continue
                if meta == 'pointcall_action':
                    row[meta] = row_original[meta].lower()
                    continue
                row[meta] = row_original[meta]
            rows.append(row)

with open(CSV_FILE_OUTPUT, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)
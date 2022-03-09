'''
    File name: pointcall_commodity.py
    Author: Guillaume Brioudes
    Date created: 2022-02-03
    Date last modified: 2022-02-07
    Python Version: 3.10.1
    Description: Get each commodity by pointcall
'''

import csv

fields = [
    'year',
    'flag',
    'pointcall',
    'homeport',
    'homeport_state_1789_fr',
    'ferme_bureau',
    'ferme_direction',
    'pointcall_province',
    'pointcall_admiralty',
    'pointcall_action',
    'commodity_standardized',
    'tonnage'
]

fields_commodity = [
    'commodity_standardized_fr',
    'commodity_standardized2_fr',
    'commodity_standardized3_fr',
    'commodity_standardized4_fr'
]

rows = []

CSV_FILE_OUTPUT = '../src/static/data/pointcall_commodity.csv'

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_pointcalls_' + year + '.csv'

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        nb_commodity = 0

        for row_original in reader:
            row = dict.fromkeys(
                fields,
                '' # initial value for all fields
            )

            tonnage = row_original['tonnage']

            for commodity in fields_commodity:
                if row_original[commodity] != '':
                    nb_commodity += 1

            for commodity in fields_commodity:
                if row_original[commodity] == '':
                    continue

                for meta in row.keys():
                    if meta == 'year':
                        row[meta] = year
                        continue
                    if meta == 'commodity_standardized':
                        row[meta] = row_original[commodity]
                        continue
                    if meta == 'pointcall_action':
                        row[meta] = row_original[meta].lower()
                        continue
                    if meta == 'tonnage':
                        try:
                            row[meta] = int(row_original[meta]) / nb_commodity
                        except:
                            row[meta] = 0
                        continue

                    row[meta] = row_original[meta]

                rows.append(row)

            nb_commodity = 0

with open(CSV_FILE_OUTPUT, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)
'''
    File name: flow.py
    Author: Guillaume Brioudes
    Date created: 2022-02-03
    Date last modified: 2022-02-03
    Python Version: 3.10.1
    Description: Get flows data with Dunkerque as departure
'''

import csv

fields = [
    'year',
    'departure',
    'destination',
    'homeport',
    'homeport_state_1789_fr',
    'flag',
    'tonnage',
    'tonnage_class',
    'commodity_standardized_fr',
    'departure_ferme_bureau',
    'departure_ferme_direction',
    'departure_province',
    'departure_admiralty',
    'departure_action',
    'destination_ferme_bureau',
    'departure_state_1789_fr',
    'destination_state_1789_fr',
    'destination_ferme_direction',
    'destination_province',
    'destination_admiralty',
    'destination_action'
]

rows = []

CSV_FILE_OUTPUT = '../src/static/data/flows.csv'

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_flows_' + year + '.csv'

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row_original in reader:
            # if row_original['departure'] != 'Dunkerque':
            #     continue

            row = dict.fromkeys(
                fields,
                '' # initial value for all fields
            )
            for meta in row.keys():
                if meta == 'year':
                    row[meta] = year
                    continue
                if meta == 'departure_action' or meta == 'destination_action' :
                    row[meta] = row_original[meta].lower()
                    continue
                row[meta] = row_original[meta]
            rows.append(row)

with open(CSV_FILE_OUTPUT, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)
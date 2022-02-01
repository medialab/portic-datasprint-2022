'''
    File name: destination.py
    Author: Guillaume Brioudes
    Date created: 2022-01-31
    Date last modified: 2022-01-31
    Python Version: 3.10.1
    Description: 
'''

import csv

fields = [
    'homeport',
    'departure_ferme_bureau',
    'destination_ferme_bureau',
    'departure_ferme_direction',
    'destination_ferme_direction',
    'departure_admiralty',
    'destination_admiralty',
    'departure_province',
    'destination_province',
    'tonnage'
]

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_flows_' + year + '.csv'
    CSV_FILE_OUTPUT = '../src/static/data/destination_' + year + '.csv'

    file = open(CSV_FILE_OUTPUT, 'w')
    writer = csv.writer(file)

    writer.writerow(fields)

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            writer.writerow([row[field].lower() for field in fields])

    file.close()
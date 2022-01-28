'''
    File name: portic.py
    Author: Guillaume Brioudes
    Date created: 2022-01-28
    Date last modified: 2022-01-28
    Python Version: 3.10.1
    Description: 
'''

import csv

fields = ['year', 'homeport', 'tonnage', 'tonnage_class', 'tonnage_uncertainity', 'departure_fr', 'cargo_item_action', 'cargo_item_action2', 'cargo_item_action3', 'cargo_item_action4', 'commodity_purpose', 'commodity_purpose2', 'commodity_purpose3', 'commodity_purpose4']

CSV_FILE_INPUT = '../data/data-portic.csv'
CSV_FILE_OUTPUT = '../src/static/data/commodity.csv'

file = open(CSV_FILE_OUTPUT, 'w')
writer = csv.writer(file)

writer.writerow(fields)

with open(CSV_FILE_INPUT, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:

        if row['homeport'] != 'Dunkerque':
            continue

        writer.writerow([row[field].lower() for field in fields])

file.close()
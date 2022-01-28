'''
    File name: product.py
    Author: Guillaume Brioudes
    Date created: 2022-01-24
    Date last modified: 2022-01-24
    Python Version: 3.10.1
    Description: For each travel to/from Dunkerque, report the product with the several classifications
'''

import json
import csv

JSON_file = open("../config.json", "r").read()
JSON = json.loads(JSON_file)

script_name = 'product'
script_data = [viz for viz in JSON['visualizations'] if viz['name'] == script_name][0]

file = open('../src/static/data/' + script_data['build']['files'][0], 'w')
writer = csv.writer(file)

fields = script_data['build']['fields']
source = script_data['source']

CSV_FIRST_LINE = ['year', 'value', 'source', 'export', 'import', 'partner'] + fields
writer.writerow(CSV_FIRST_LINE)

with open('../data/' + source, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:

        if row['best_guess_region_prodxpart'] != '1':
            continue
        row['partner'] = row['partner'].lower()
        if row['partner'].find('dunkerque') == -1:
            continue

        writer.writerow(
            [
                row['year'],
                row['value'],
                'best_guess_region_prodxpart', # seule
                'yes' if row['export_import'] == 'Exports' else 'no',
                'yes' if row['export_import'] == 'Imports' else 'no',
                row['partner']
            ]
            +
            [row[field] for field in fields]
        )

file.close()
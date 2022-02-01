'''
    File name: product.py
    Author: Guillaume Brioudes
    Date created: 2022-01-24
    Date last modified: 2022-01-28
    Python Version: 3.10.1
    Description: For each travel to/from Dunkerque, report the product with the several classifications
'''

import csv

CSV_FILE_INPUT = '../data/toflit18_all.csv'
CSV_FILE_OUTPUT = '../src/static/data/product.csv'

file = open(CSV_FILE_OUTPUT, 'w')
writer = csv.writer(file)

fields = [
    'product',
    'product_revolutionempire',
    'product_simplification',
    'product_sitc_FR',
    'product_RE_aggregate',
    'customs_region',
    'customs_office',
    'origin',
    'origin_province',
    'origin_source'
]

CSV_FIRST_LINE = ['year', 'value', 'source', 'export', 'import', 'partner'] + fields
writer.writerow(CSV_FIRST_LINE)

with open(CSV_FILE_INPUT, newline='') as csvfile:
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
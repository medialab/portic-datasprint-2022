'''
    File name: commodity.py
    Author: Guillaume Brioudes
    Date created: 2022-01-28
    Date last modified: 2022-01-28
    Python Version: 3.10.1
    Description: Get columns for analyse the tonnage and the commodity of Dunkerque attached ships
'''

import csv

fields = [
    'homeport',
    'tonnage',
    'destination_fr',
    'departure_fr',
    'cargo_item_action',
    'cargo_item_action2',
    'cargo_item_action3',
    'cargo_item_action4',
    'commodity_standardized_fr'
]

fields_commodity = [
    'commodity_purpose',
    'commodity_purpose2',
    'commodity_purpose3',
    'commodity_purpose4'
]

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_flows_' + year + '.csv'

    file_data = open('../src/static/data/commodity_data_' + year + '.csv', 'w')
    writer_data = csv.writer(file_data)
    writer_data.writerow(fields)

    file_purpose = open('../src/static/data/commodity_purpose_' + year + '.csv', 'w')
    writer_purpose = csv.writer(file_purpose)
    writer_purpose.writerow(['produit', 'nb_boat'])
    commodities = {}

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            if row['homeport'] != 'Dunkerque':
                continue

            writer_data.writerow([row[field].lower() for field in fields])

            for content in fields_commodity:
                commodity = row[content]
                if commodity in commodities:
                    commodities[commodity] += 1
                else:
                    commodities[commodity] = 1

    for commodity in commodities.keys():
        writer_purpose.writerow([commodity, commodities[commodity]])

    file_data.close()
    file_purpose.close()
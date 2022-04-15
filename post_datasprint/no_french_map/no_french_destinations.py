import csv

CSV_FILE_INPUT_1787 = '../../data/navigo_all_flows_1787.csv'
CSV_FILE_INPUT_1789 = '../../data/navigo_all_flows_1789.csv'

no_french_ship_destinations = {}

"""
destinations des navires de pavillon étranger (= tout ce qui n'est pas = French) avec possibilité ajouter ET Taxe CONTIENT "long cours"  
"""

for source in [CSV_FILE_INPUT_1787]:

    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['flag'] == 'French':
                continue
            if 'long cours' not in row['all_taxes']:
                continue
            if row['destination'] == '':
                continue
            
            if row['destination'] in no_french_ship_destinations:
                no_french_ship_destinations[row['destination']]['occurence'] += 1
            else:
                no_french_ship_destinations[row['destination']] = {
                    'occurence': 1,
                    'uhgs_id': row['destination_uhgs_id'],
                    'latitude': row['destination_latitude'],
                    'longitude': row['destination_longitude']
                }

with open('no_french_destinations.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'uhgs_id',
        'destination',
        'occurence',
        'latitude',
        'longitude'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for destination in no_french_ship_destinations.keys():
        item = no_french_ship_destinations[destination]

        writer.writerow({
            'uhgs_id': item['uhgs_id'],
            'destination': destination,
            'occurence': item['occurence'],
            'latitude': item['latitude'],
            'longitude': item['longitude'],
        })
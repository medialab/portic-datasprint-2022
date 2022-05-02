import csv

CSV_FILE_INPUT_1787 = '../../data/navigo_all_flows_1787.csv'
CSV_FILE_INPUT_1789 = '../../data/navigo_all_flows_1789.csv'

no_french_ship_flows = []

"""
destinations des navires de pavillon étranger (= tout ce qui n'est pas = French) avec possibilité ajouter ET Taxe CONTIENT "long cours"  
"""

for source in [CSV_FILE_INPUT_1787]:

    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['flag'] != 'French':
                continue
            if row['departure'] != 'Dunkerque':
                continue
            if 'long cours' not in row['all_taxes']:
                continue
            
            no_french_ship_flows.append(row)

with open('french_map.csv', 'w', newline='') as csvfile:
    fieldnames = {
        'departure',
        'departure_uhgs_id',
        'departure_latitude',
        'departure_longitude',
        'destination',
        'destination_uhgs_id',
        'destination_latitude',
        'destination_longitude',
        'tonnage'
    }

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for flow in no_french_ship_flows:
        flow = {key: value for key, value in flow.items() if key in fieldnames}
        writer.writerow(flow)
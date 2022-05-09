"""
dictionnaire trop limitant, il faut dénombrer
"""

import csv
import geocoder

navigo = {}
destination_state_1789_fr = {}
destination_substate_1789_fr = {}

with open('../../data/navigo_all_flows_1787.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['destination_uhgs_id'] in navigo:
            navigo[row['destination_uhgs_id']].append(row)
        else:
            navigo[row['destination_uhgs_id']] = [row]

with open('is_gb_uhgs_id.csv', 'w', newline='') as csvfile:
    fieldnames = {
        'destination_uhgs_id',
        'port',
        'destination_state_1789_fr',
        'destination_substate_1789_fr'
    }
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    with open('CUST-17-11_1_page 22_inward.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rest = set()
        for row in reader:
            if row['uhgs_id'] == '#N/A':
                rest.add(row['Names of the ports'])
                continue
            if row['uhgs_id'] not in navigo:
                rest.add(row['Names of the ports'])
                continue
            navigo_rows = navigo[row['uhgs_id']]

            navigo_rows_destination_state_1789_fr = set([row['destination_state_1789_fr'] for row in navigo_rows])
            navigo_rows_destination_substate_1789_fr = set([row['destination_substate_1789_fr'] for row in navigo_rows])

            writer.writerow({
                'destination_uhgs_id': row['uhgs_id'],
                'port': row['Names of the ports'],
                'destination_state_1789_fr': list(navigo_rows_destination_state_1789_fr)[0],
                'destination_substate_1789_fr': list(navigo_rows_destination_substate_1789_fr)[0]
            })
        for port_name in rest:
            g = geocoder.geonames(port_name, lang='fr', key='myllaume', maxRows=5, country='GB')
            for r in g:
                country = r.country
                state = r.state
                if country == 'Royaume Uni':
                    writer.writerow({
                        'destination_uhgs_id': '',
                        'port': port_name,
                        'destination_state_1789_fr': 'Grande-Bretagne',
                        'destination_substate_1789_fr': state
                    })
                    break
import csv

"""
True si la destination est la Grande-Bretagne et non les colonies anglaises à travers le monde
"""
def is_gb_destination(row):
    row['destination_substate_1789_fr'] = row['destination_substate_1789_fr'].lower()

    if row['destination_state_1789_fr'] == 'Grande-Bretagne' \
        and 'colonies britanniques' not in row['destination_substate_1789_fr']:
        return True
    return False

nb_departure = 0

with open('../../data/navigo_all_flows_1787.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if is_gb_destination(row) == False:
            continue
        if row['departure_province'] == 'Flandre':
            continue
        if row['commodity_id'] not in {'00000162', '00000469', '00000094'}:
            continue
        nb_departure += 1

print(nb_departure)
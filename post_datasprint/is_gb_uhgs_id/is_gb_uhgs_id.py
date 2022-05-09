import csv

navigo = {}
destination_state_1789_fr = set()
destination_substate_1789_fr = set()
destination = set()

with open('../../data/navigo_all_flows_1787.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        navigo[row['destination_uhgs_id']] = row

with open('CUST-17-11_1_page 22_inward.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['uhgs_id'] == '#N/A':
            continue
        if row['uhgs_id'] not in navigo:
            continue
        navigo_row = navigo[row['uhgs_id']]
        destination_state_1789_fr.add(navigo_row['destination_state_1789_fr'])
        destination_substate_1789_fr.add(navigo_row['destination_substate_1789_fr'])
        destination.add(navigo_row['destination'])

print(destination_state_1789_fr)
print(destination_substate_1789_fr)
print(destination)
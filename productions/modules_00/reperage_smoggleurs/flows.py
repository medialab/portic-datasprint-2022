from mdutils.mdutils import MdUtils
import csv
import json
from pprint import pprint

CSV_FILE_INPUT = '../../../data/navigo_all_flows_1787.csv'
# JSON_FILE_OUTPUT = 'smoggleurs-product.json'

departs = {}
arrivee_grande_bretagne = {}

with open(CSV_FILE_INPUT, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['departure_state_1789_fr'] != 'France':
            continue

        if row['departure_fr'] in departs:
            departs[row['departure_fr']]['total'] += 1
            if row['destination_state_1789_fr'] == 'Grande-Bretagne':
                departs[row['departure_fr']]['dont_vers_grande_bretagne'] += 1
            else:
                departs[row['departure_fr']]['dont_vers_grande_bretagne'] += 0
        else:
            departs[row['departure_fr']] = {
                'name': row['departure_fr'],
                'total': 1,
                'dont_vers_grande_bretagne': 1 if row['destination_state_1789_fr'] == 'Grande-Bretagne' else 0,
                'per_cent': 0
            }

for port in departs.keys():
    total = departs[port]['total']
    nb_vers_gb = departs[port]['dont_vers_grande_bretagne']
    departs[port]['per_cent'] = (nb_vers_gb / total) * 100

depart_sorted = [departs[key] for key in departs.keys()]
depart_sorted = sorted(depart_sorted, key=lambda d: d['per_cent'])[::-1]

mdFile = MdUtils(file_name='departs_port_france', title='Départ des ports de France')

mdFile.new_paragraph("Année 1787")
mdFile.new_line("")
mdFile.new_line( "| Nom port | nombre de départ | dont vers l'angleterre | % ")
mdFile.new_line( "| --- | --- | --- | --- |")
for depart in depart_sorted:
    name = depart['name']
    total = depart['total']
    nb_vers_gb = depart['dont_vers_grande_bretagne']
    per_cent = depart['per_cent']
    mdFile.new_line( "| " + name + " | " + str(total)  + " | " + str(nb_vers_gb)  + " | " + str(round(per_cent)) + " |" )

mdFile.create_md_file()
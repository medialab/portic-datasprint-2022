from mdutils.mdutils import MdUtils
import csv
import json
from pprint import pprint

CSV_FILE_INPUT = '../../../data/navigo_all_flows_1787.csv'

departs = {}

with open(CSV_FILE_INPUT, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # COLLECTE DES DEPARTS

    for row in reader:
        if row['departure_state_1789_fr'] != 'France' or row['departure_function'] != 'O':
            continue

        row['tonnage'] = int(row['tonnage']) if row['tonnage'].isnumeric() == True else 0

        if row['departure_fr'] in departs:
            departs[row['departure_fr']]['total'] += 1
            if row['destination_state_1789_fr'] == 'Grande-Bretagne':
                departs[row['departure_fr']]['dont_vers_grande_bretagne'] += 1
                departs[row['departure_fr']]['tonnage_vers_grande_bretagne'] += row['tonnage']
                if row['flag'] == 'British':
                    departs[row['departure_fr']]['nb_bateau_anglais'] += 1
                    departs[row['departure_fr']]['tonnage_bateaux_anglais_vers_grande_bretagne'] += row['tonnage']
        else:
            departs[row['departure_fr']] = {
                'name': row['departure_fr'],
                'total': 1,
                'dont_vers_grande_bretagne': 1 if row['destination_state_1789_fr'] == 'Grande-Bretagne' else 0,
                'tonnage_vers_grande_bretagne': row['tonnage'] if row['destination_state_1789_fr'] == 'Grande-Bretagne' else 0,
                'nb_bateau_anglais': 1 if row['flag'] == 'British' else 0,
                'tonnage_bateaux_anglais_vers_grande_bretagne': row['tonnage'] if row['flag'] == 'British' else 0,
                'per_cent': 0,
                'per_cent_bateaux_anglais': 0,
                'per_cent_tonnage_bateaux_anglais': 0
            }

# CALCUL DES %

for port in departs.keys():
    if departs[port]['dont_vers_grande_bretagne'] == 0:
        continue

    total = departs[port]['total']
    nb_vers_gb = departs[port]['dont_vers_grande_bretagne']
    # % du total des bateaux qui vont vers l'Angleterre
    departs[port]['per_cent'] = (nb_vers_gb / total) * 100

    nb_bateau_anglais = departs[port]['nb_bateau_anglais']
    # % des bateaux qui vont vers l'Angleterre qui sont anglais
    departs[port]['per_cent_bateaux_anglais'] = (nb_bateau_anglais / nb_vers_gb) * 100

    tonnage = departs[port]['tonnage_vers_grande_bretagne']
    tonnage_anglais = departs[port]['tonnage_bateaux_anglais_vers_grande_bretagne']
    # % du tonnage de bateaux qui vont vers l'Angleterre qui sont anglais
    departs[port]['per_cent_tonnage_bateaux_anglais'] = (tonnage_anglais / tonnage) * 100

# FILTRE ET TRI

depart_sorted = [departs[key] for key in departs.keys() if departs[key]['dont_vers_grande_bretagne'] > 0]
depart_sorted = sorted(depart_sorted, key=lambda d: d['per_cent'])[::-1]

# RENDU EN CSV

with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'Nom port',
        'nombre de départ',
        "dont vers l'angleterre",
        "% départs vers angleterre",
        "nombre de bateaux anglais",
        "% bateaux anglais avec départ angleterre",
        "tonnage bateaux vers angleterre",
        "tonnage des bateaux anglais vers angleterre",
        "% tonnage anglais vers angleterre"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for depart in depart_sorted:
        writer.writerow(
            {
                'Nom port': depart['name'],
                'nombre de départ': depart['total'],
                "dont vers l'angleterre": depart['dont_vers_grande_bretagne'],
                "% départs vers angleterre": depart['per_cent'],
                "nombre de bateaux anglais": depart['nb_bateau_anglais'],
                "% bateaux anglais avec départ angleterre": depart['per_cent_bateaux_anglais'],
                "tonnage bateaux vers angleterre": depart['tonnage_vers_grande_bretagne'],
                "tonnage des bateaux anglais vers angleterre": depart['tonnage_bateaux_anglais_vers_grande_bretagne'],
                "% tonnage anglais vers angleterre": depart['per_cent_tonnage_bateaux_anglais']
            }
        )
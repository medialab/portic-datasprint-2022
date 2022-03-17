import csv
from functions import is_smoggleur_dunkerque, is_smoggleur_calais, is_smoggleur_boulogne, is_smoggleur_roscoff, is_smoggleur_lorient, is_smoggleur_bordeaux

CSV_FILE_INPUT_1787 = '../../data/navigo_all_flows_1787.csv'
CSV_FILE_INPUT_1789 = '../../data/navigo_all_flows_1789.csv'

# Contient tous les flows du port éponyme
dunkerque = []
calais = []
boulogne = []
roscoff = []
lorient = []
bordeaux = []

for source in [CSV_FILE_INPUT_1787]:

    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            row['tonnage'] = int(row['tonnage']) if row['tonnage'].isnumeric() == True else 0

            if row['departure_fr'] == 'Dunkerque':
                row['is_smoggleur'] = is_smoggleur_dunkerque(row)
                dunkerque.append(row)
            if row['departure_fr'] == 'Calais':
                row['is_smoggleur'] = is_smoggleur_calais(row)
                calais.append(row)
            if row['departure_fr'] == 'Boulogne-sur-Mer':
                row['is_smoggleur'] = is_smoggleur_boulogne(row)
                boulogne.append(row)
            if row['departure_fr'] == 'Roscoff':
                row['is_smoggleur'] = is_smoggleur_roscoff(row)
                roscoff.append(row)
            if row['departure_fr'] == 'Lorient':
                row['is_smoggleur'] = is_smoggleur_lorient(row)
                lorient.append(row)
            if row['departure_fr'] == 'Bordeaux':
                row['is_smoggleur'] = is_smoggleur_bordeaux(row)
                bordeaux.append(row)

with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'departure_fr',
        'departure_longitude',
        'departure_latitude',
        'destination_fr',
        'destination_longitude',
        'destination_latitude',
        'tonnage',
        'is_smoggleur'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for flow in dunkerque + calais + boulogne + roscoff + lorient + bordeaux:
        if flow['flag'] != 'British':
            continue
        if flow['destination_fr'] in {'Angleterre', 'Angleterre (destination simulée pour)'}:
            flow['destination_fr'] = 'Autre en Angleterre'
            # continue
        if flow['destination_fr'] in {'pas identifié', 'pas mentionné'}:
            flow['destination_fr'] = 'inconnu'
            # continue
        if flow['is_smoggleur'] == False:
            continue
        writer.writerow({
            'departure_fr': flow['departure_fr'],
            'departure_longitude': flow['departure_longitude'],
            'departure_latitude': flow['departure_latitude'],
            'destination_fr': flow['destination_fr'],
            'destination_longitude': flow['destination_longitude'],
            'destination_latitude': flow['destination_latitude'],
            'tonnage': flow['tonnage'],
            'is_smoggleur': 1 if flow['is_smoggleur'] == True else 0
        })
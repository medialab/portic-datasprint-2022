import csv
from functions import is_smoggleur_dunkerque, is_smoggleur_calais, is_smoggleur_boulogne, is_smoggleur_roscoff, is_smoggleur_lorient, is_smoggleur_bordeaux, is_illegal_commodities

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

with open('smoggleurs.csv', 'w', newline='') as csvfile:
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
        # if flow['is_smoggleur'] == False:
        #     continue
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

ports = {
    'dunkerque': dunkerque,
    'calais': calais,
    'boulogne': boulogne,
    'roscoff': roscoff,
    'lorient': lorient,
    'bordeaux': bordeaux,
}

with open('ports.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'port de départ',
        'total des trajets anglais',
        'trajets anglais smoggleurs',
        '% de trajets anglais smoggleurs',
        'total tonnage',
        'tonnage smoggleur',
        '% de tonnage smoggleurs',
        'total des destinations',
        'destinations smoggleurs',
        '% de destination smoggleurs',
        'smoggleurs avec produits de contrebande',
        '% de smoggleurs avec produits de contrebande'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for port in ports.keys():
        flows = [flow for flow in ports[port] if flow['flag'] == 'British']

        row = dict.fromkeys(
            fieldnames,
            0 # initial value for all fields
        )

        row['port de départ'] = port
        row['total des trajets anglais'] = len(flows)
        row['trajets anglais smoggleurs'] = len([flow for flow in ports[port] if flow['is_smoggleur'] == True])
        row['% de trajets anglais smoggleurs'] = (row['trajets anglais smoggleurs'] / row['total des trajets anglais']) * 100
        row['total tonnage'] = sum([flow['tonnage'] for flow in ports[port]])
        row['tonnage smoggleur'] = sum([flow['tonnage'] for flow in ports[port] if flow['is_smoggleur'] == True])
        row['% de tonnage smoggleurs'] = (row['tonnage smoggleur'] / row['total tonnage']) * 100
        row['total des destinations'] = len(set([flow['destination_fr'] for flow in ports[port]]))
        row['destinations smoggleurs'] = len(set([flow['destination_fr'] for flow in ports[port] if flow['is_smoggleur'] == True]))
        row['% de destination smoggleurs'] = (row['destinations smoggleurs'] / row['total des destinations']) * 100
        row['smoggleurs avec produits de contrebande'] = len([flow for flow in ports[port] if (flow['is_smoggleur'] == True and is_illegal_commodities(flow) == True)])
        row['% de destination smoggleurs'] = 0 if row['smoggleurs avec produits de contrebande'] == 0 else (row['smoggleurs avec produits de contrebande'] / row['trajets anglais smoggleurs']) * 100

        writer.writerow(row)

with open('produits.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'port de départ',
        'port de destination',
        'produit',
        'tonnage pondéré'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for flow in dunkerque + calais + boulogne + roscoff + lorient + bordeaux:
        if flow['is_smoggleur'] == False:
            continue

        commodities = [flow['commodity_standardized_fr'], flow['commodity_standardized2_fr'], flow['commodity_standardized3_fr'], flow['commodity_standardized4_fr']]
        commodities = [commodity for commodity in commodities if commodity != '']

        for commodity in commodities:

            writer.writerow({
                'port de départ': flow['departure_fr'],
                'port de destination': flow['destination_fr'],
                'produit': commodity,
                'tonnage pondéré': flow['tonnage'] / len(commodities)
            })
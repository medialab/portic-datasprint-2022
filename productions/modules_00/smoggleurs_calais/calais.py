import csv
from pprint import pprint

CSV_FILE_INPUT = '../../../data/navigo_all_flows_1787.csv'

destination_depuis_calais = {}
tonnages_depuis_calais = {}

def is_gb_destination(row):
    row['destination_substate_1789_fr'] = row['destination_substate_1789_fr'].lower()

    if row['destination_state_1789_fr'] == 'Grande-Bretagne' \
        and 'colonies britanniques' not in row['destination_substate_1789_fr']:
        return True
    
    return False

with open(CSV_FILE_INPUT, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # COLLECTE DES DEPARTS

    for row in reader:
        if row['departure_fr'] != 'Calais' or is_gb_destination(row) == False:
            continue

        row['tonnage'] = int(row['tonnage']) if row['tonnage'].isnumeric() == True else 0

        if row['tonnage'] in tonnages_depuis_calais:
            tonnages_depuis_calais[row['tonnage']] += 1
        else:
            tonnages_depuis_calais[row['tonnage']] = 1

        if row['destination_fr'] in destination_depuis_calais:
            destination_depuis_calais[row['destination_fr']]['occurence'] += 1
            destination_depuis_calais[row['destination_fr']]['tonnage_cumule'] += row['tonnage']
            destination_depuis_calais[row['destination_fr']]['tonnage_class'][row['tonnage_class']] += 1
        else:
            destination_depuis_calais[row['destination_fr']] = {
                'occurence': 1,
                'tonnage_cumule': row['tonnage'],
                'tonnage_class': {
                    '[1-20]': 0,
                    '[21-50]': 0,
                    '[51-100]': 0,
                    '[101-200]': 0,
                    '[201-500]': 0
                }
            }

            destination_depuis_calais[row['destination_fr']]['tonnage_class'][row['tonnage_class']] = 1
pprint(destination_depuis_calais)

with open('result_destination.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'Port de destination',
        'Nombre de départs vers le port de destination',
        'Tonnage cumulé vers le port de destination',
        'Nombre de bateau avec une classe de [1-20]',
        'Nombre de bateau avec une classe de [21-50]',
        'Nombre de bateau avec une classe de [51-100]',
        'Nombre de bateau avec une classe de [101-200]',
        'Nombre de bateau avec une classe de [201-500]'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for destination in destination_depuis_calais.keys():
        writer.writerow(
            {
                'Port de destination': destination,
                'Nombre de départs vers le port de destination': destination_depuis_calais[destination]['occurence'],
                'Tonnage cumulé vers le port de destination': destination_depuis_calais[destination]['tonnage_cumule'],
                'Nombre de bateau avec une classe de [1-20]': destination_depuis_calais[destination]['tonnage_class']['[1-20]'] / destination_depuis_calais[destination]['occurence'],
                'Nombre de bateau avec une classe de [21-50]': destination_depuis_calais[destination]['tonnage_class']['[21-50]'] / destination_depuis_calais[destination]['occurence'],
                'Nombre de bateau avec une classe de [51-100]': destination_depuis_calais[destination]['tonnage_class']['[51-100]'] / destination_depuis_calais[destination]['occurence'],
                'Nombre de bateau avec une classe de [101-200]': destination_depuis_calais[destination]['tonnage_class']['[101-200]'] / destination_depuis_calais[destination]['occurence'],
                'Nombre de bateau avec une classe de [201-500]': destination_depuis_calais[destination]['tonnage_class']['[201-500]'] / destination_depuis_calais[destination]['occurence'],
            }
        )

with open('result_tonnage.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'tonnage',
        'occurences'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for tonnage, occurence in tonnages_depuis_calais.items():
        writer.writerow(
            {
                'tonnage': tonnage,
                'occurences': occurence
            }
        )
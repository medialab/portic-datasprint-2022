import csv
from functions import is_smoggleur_dunkerque, is_smoggleur_calais, is_smoggleur_boulogne, is_smoggleur_roscoff, is_smoggleur_lorient, is_smoggleur_bordeaux

CSV_FILE_INPUT_1787 = '../../data/navigo_all_flows_1787.csv'
CSV_FILE_INPUT_1789 = '../../data/navigo_all_flows_1789.csv'

smoggleurs_from_dunkerque = []
smoggleurs_from_calais = []
smoggleurs_from_boulogne = []
smoggleurs_from_roscoff = []
smoggleurs_from_lorient = []
smoggleurs_from_bordeaux = []

for source in [CSV_FILE_INPUT_1787, CSV_FILE_INPUT_1789]:

    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            row['tonnage'] = int(row['tonnage']) if row['tonnage'].isnumeric() == True else 0
            
            if is_smoggleur_dunkerque(row) == True:
                smoggleurs_from_dunkerque.append(row)
            if is_smoggleur_calais(row) == True:
                smoggleurs_from_calais.append(row)
            if is_smoggleur_boulogne(row) == True:
                smoggleurs_from_boulogne.append(row)
            if is_smoggleur_roscoff(row) == True:
                smoggleurs_from_roscoff.append(row)
            if is_smoggleur_lorient(row) == True:
                smoggleurs_from_lorient.append(row)
            if is_smoggleur_bordeaux(row) == True:
                smoggleurs_from_bordeaux.append(row)
print(
    len(smoggleurs_from_dunkerque),
    len(smoggleurs_from_calais),
    len(smoggleurs_from_boulogne),
    len(smoggleurs_from_roscoff),
    len(smoggleurs_from_lorient),
    len(smoggleurs_from_bordeaux),
)
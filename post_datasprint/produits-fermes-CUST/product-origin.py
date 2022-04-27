"""
description: https://github.com/medialab/portic-datasprint-2022/issues/3#issue-1184954966
"""

import csv

product_classfication = 'product_revolutionempire'
ports_smoggleurs = {'Dunkerque', 'Calais', 'Bordeaux', 'Boulogne sur Mer', 'Roscoff', 'Lorient'}
ports_smoggleurs.remove('Dunkerque')
bureau_ferme_smoggleur = set()
product_ports_smoggleurs = {}

with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['best_guess_region_prodxpart'] != '1':
            continue
        if row['year'] != '1789':
            continue
        if row['export_import'] != 'Exports':
            continue

        for port_smoggleur in ports_smoggleurs:
            if port_smoggleur.lower() in row['partner'].lower():
                bureau_ferme_smoggleur.add(row['customs_office'])
                if row[product_classfication] in product_ports_smoggleurs:
                    product_ports_smoggleurs[row[product_classfication]] += 1
                else:
                    product_ports_smoggleurs[row[product_classfication]] = 1

# sort
product_ports_smoggleurs = {k: v for k, v in sorted(product_ports_smoggleurs.items(), key=lambda item: item[1], reverse=True)}

with open('product-smoggleur-ports.csv', 'w', newline='') as csvfile:
    fieldnames = {
        'product',
        'occurences'
    }

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for product in product_ports_smoggleurs.keys():
        writer.writerow({
            'product': product,
            'occurences': product_ports_smoggleurs[product]
        })


# sorties_Dunkerque_Etranger_1789.csv.csv

import csv
import json

by_pointcalls = []
by_ports = []

with open('./sorties_Dunkerque_Etranger_1789.csv.csv', 'r') as f:
  reader = csv.DictReader(f, delimiter=";")
  for row in reader:
    if row['all_cargos'] != '':
      cargos = json.loads(row['all_cargos'])
      for cargo in cargos:
        by_pointcalls.append({
          "cargo": cargo['commodity_purpose'],
          "cargo_standardized_fr": cargo['commodity_standardized_fr'],
          **row
        })
    else:
      by_pointcalls.append({
        "cargo": "",
        "cargo_standardized_fr": "",
        **row
      })

fieldnames = by_pointcalls[0].keys()
with open('./sorties_Dunkerque_Etranger_1789_par_produit.csv', 'w') as f:
  w = csv.DictWriter(f, fieldnames=fieldnames)
  w.writeheader()
  for p in by_pointcalls:
    w.writerow(p)


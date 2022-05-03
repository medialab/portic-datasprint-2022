import csv


# 1. calculer les valeurs d'exports par partenaire
toflit_map = {}
with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  # ouvrir les flux de toflit
  for row in reader:
    # filtrer 89 + bureau des fermes de La Rochelle + exports
    if row['year'] == '1789' and row['customs_office'] == 'La Rochelle' and row['export_import'] == 'Exports':
      partner = row['partner_simplification']
      if partner == "États de l'Empereur":
        partner = "Etats de l'Empereur"
      if partner == "Villes hanséatiques":
        partner = "Quatre villes hanséatiques"
      value = float(row['value'] or 0)
      if partner not in toflit_map:
        toflit_map[partner] = 0
      # grouper par partenaire_simplification et sommer les valeurs
      toflit_map[partner] += value

# 2. faire une map des tonnages pour la rochelle - '../../productions/module_12/export_france_1789_par_pays_par_produits.csv'
navigo_map = {}
with open('../../productions/module_12/suite_export_laRochelle_1789_par_pays_par_produits.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    partner = row['destination_partner_balance_1789']
    navigo_map[partner] = float(row['sum_tonnage'])

output = []
print("toflit map:")
print(toflit_map)
print("navigo map:")
print(navigo_map)
# 3. reprojeter la map des tonnages sur des prix
with open('cross_navigo_toflit_by_destination.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    partner = row['partner']
    price= float(row['price_per_barrel'])
    if partner in navigo_map and partner in toflit_map:
      tonnage = navigo_map[partner]
      projected_price = tonnage * price
      price_toflit18 = toflit_map[partner]
      output.append({
        "partner": partner,
        "price_toflit18" : price_toflit18,
        "projected_price": projected_price
      })
    else:
      print("no match for", partner)

print("output", output)
with open('projection_la_rochelle_89.csv', 'w') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=['partner', 'price_toflit18', 'projected_price'])
  writer.writeheader()
  for row in output:
    writer.writerow(row)
import csv

rows_navigo = []
rows_toflit = []

rows_terremer = {}

destinations_navigo = {}
with open('../../data/navigo_all_flows_1787.csv', newline='') as csvfile:
  flows = csv.DictReader(csvfile)
  commodity_fields = ['commodity_standardized_fr', 'commodity_standardized2_fr', 'commodity_standardized3_fr', 'commodity_standardized4_fr']
  stop_commodities = set(['lest', 'lège', 'vide', 'futailles vides'])
  total_commodities = set()
  for flow in flows:
    destination = flow['destination_partner_balance_1789']
    transformation_map = {
      'Quatre villes hanséatiques': 'Villes hanséatiques',
      'Etats-Unis': 'États-Unis d\'Amérique',
      # 'Etats de l\'Empereur':''
    }
    if destination in transformation_map:
      destination = transformation_map[destination]
    departure = flow['departure_state_1789_fr']
    tonnage = float(flow['tonnage'] or 0)
    if flow['departure_function'] == 'O' \
      and departure == 'France' \
      and destination != '' \
      and destination != 'France' \
      and flow['destination_state_1789_fr'] != 'France' :
      commodities = [flow[field].lower() for field in commodity_fields if flow[field] != '']
      not_stop = [commodity for commodity in commodities if commodity not in stop_commodities]
      if len(commodities) == 0 or len(not_stop) > 0:
        for c in not_stop:
          total_commodities.add(c)
        # print(departure + '->' + destination, flow['tonnage'] + '->' + str(tonnage))
        # at this point we have all the flows we want
        if destination not in destinations_navigo:
          destinations_navigo[destination] = 0
        destinations_navigo[destination] += tonnage
      # else:
      #   print('removing flow with commodities :', commodities)
print('destinations navigo:')
print(destinations_navigo)
# print([{"destination": destination, "tonnage": tonnage} for destination, tonnage in destinations_navigo.items()])

# for control
# print('\n'.join(sorted(list(total_commodities))))
# for control
with open('../../productions/module_12/export_france_1787_par_pays_par_produits.csv', newline='') as csvfile:
    rows_navigo = list(csv.DictReader(csvfile))
    control_map = {}
    for flow in rows_navigo:
      destination = flow["destination_partner_balance_1789"]
      tonnage = float(flow["sum_tonnage"] or 0)
      if destination not in control_map:
        control_map[destination] = 0
      control_map[destination] += tonnage
print("control map navigo:")
print(control_map)

# with open('./tolift_export_values_resume.csv', newline='') as csvfile:
#     reader_toflit = list(csv.DictReader(csvfile))
partners_toflit18 = {}
with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
  flows = csv.DictReader(csvfile)
  for flow in flows:
    if flow['source_type'] == 'Résumé' \
      and flow['year'] == '1787' \
      and flow['export_import'] != 'Exports':

      partner = flow['partner_simplification']
      value = float(flow['value'] or 0)
      if partner not in partners_toflit18:
        partners_toflit18[partner] = 0
      partners_toflit18[partner] += value
print('partners_toflit18:')
print(partners_toflit18)

with open('./terre_mer.csv', newline='') as csvfile:
    rows_terremer = list(csv.DictReader(csvfile))

terre_mer = {}
for row in rows_terremer:
  if row['partner'] not in terre_mer:
    partner = row['partner']
    transformation_map = {
      'Villes Anséatiques': 'Villes hanséatiques',
      'Danemarck et Norwège': 'Danemark',
      'République de Gênes': 'Gênes',
      'Naples et Sicile': 'Naples',
      'États du Roi de Sardaigne': 'Royaume de Sardaigne',
      'Angleterre, Ecosse et Irlande': 'Angleterre',
      'Rome et Venise': 'Venise',
      'États de l\'Empereur, en Flandre et Allemagne': 'Allemagne',
      'Suisse, ses Alliées et Genève': 'Suisse'
    }
    if partner in transformation_map:
      partner = transformation_map[partner]
    terre_mer[partner] = float(row['ratio_terre_mer'])
# print('terre mer map:')
# print(terre_mer)

partners_toflit18_corrected = {}
for (partner, value) in partners_toflit18.items():
  ratio = 1
  
  if partner in terre_mer:
    ratio = float(terre_mer[partner])
  # else:
  #   print('ratio : issue with partner: ', partner)
  partners_toflit18_corrected[partner] = value * ratio

correspondance = []
for destination, tonnage in destinations_navigo.items():
  if destination not in partners_toflit18:
    print('issue, this navigo destination country (1787) is not in toflit18 for 1787 :', destination)
  else:
    value = partners_toflit18[destination]
    correspondance.append({
      "partner": destination,
      "sum_tonnage": tonnage,
      "sum_exports": value,
      "price_per_barrel": value / tonnage
    })
with open('cross_navigo_toflit_by_destination_2.csv', 'w', newline='') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=[
      'partner',
      'sum_tonnage',
      'sum_exports',
      "price_per_barrel"
  ])
  writer.writeheader()
  for row in correspondance:
    writer.writerow(row)

# with open('cross_navigo_toflit_by_destination.csv', 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames={
#         'partner',
#         'sum_tonnage',
#         'sum_exports',
#         "price_per_barrel"
#     })
#     writer.writeheader()

#     terre_mer = {}
#     for row in rows_terremer:
#       if row['partner'] not in terre_mer:
#         terre_mer[row['partner']] = float(row['ratio_terre_mer'])

#     toflit_exports_by_partner = {}
#     for export in reader_toflit:
#       partner = export['partner_simplification']
#       if partner == "États-Unis d'Amérique":
#         partner = 'Etats-Unis'
#       value = float(export['value']) if export['value'] != '' else 0
#       ratio_key = partner
#       in_terre_mer = True
#       if partner not in terre_mer:
#         in_terre_mer = False
#         for r in terre_mer.keys():
#           lower_case = r.lower()
#           if partner.lower() in lower_case:
#             ratio_key = r
#             in_terre_mer = True
#       if in_terre_mer:
#         ratio = terre_mer[ratio_key]
#         value = value * ratio
      
#       if partner not in toflit_exports_by_partner:
#         toflit_exports_by_partner[partner] = 0
#       toflit_exports_by_partner[partner] += value
#     navigo_exports_by_partner = {}
#     for export in rows_navigo:
#       partner = export['destination_partner_balance_1789']
#       value = float(export['sum_tonnage']) if export['sum_tonnage'] != '' else 0
#       if partner not in navigo_exports_by_partner:
#         navigo_exports_by_partner[partner] = 0
#       navigo_exports_by_partner[partner] += value
#     print(toflit_exports_by_partner)
#     for (partner, sum_tonnage) in navigo_exports_by_partner.items():
#       if partner not in toflit_exports_by_partner:
#         print('this partner is not in toflit: ' + partner)
#       else:
#         sum_exports = toflit_exports_by_partner[partner]
#       writer.writerow({
#         "partner": partner,
#         "sum_tonnage": sum_tonnage,
#         "sum_exports": sum_exports,
#         "price_per_barrel": sum_exports / sum_tonnage
#       })

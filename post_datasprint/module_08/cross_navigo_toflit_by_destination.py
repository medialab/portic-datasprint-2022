import csv

rows_navigo = []
rows_toflit = []

rows_terremer = {}

with open('../../productions/module_12/export_france_1787_par_pays_par_produits.csv', newline='') as csvfile:
    # reader_navigo = csv.DictReader(csvfile)
    # for row in reader_navigo:
    #     rows_navigo.append(row)
    rows_navigo = list(csv.DictReader(csvfile))

# with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
#     reader_toflit = csv.DictReader(csvfile)
#     for row in reader_toflit:
#         rows_toflit.append(row)
with open('./tolift_export_values_resume.csv', newline='') as csvfile:
    reader_toflit = list(csv.DictReader(csvfile))

with open('./terre_mer.csv', newline='') as csvfile:
    rows_terremer = list(csv.DictReader(csvfile))


with open('cross_navigo_toflit_by_destination.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames={
        'partner',
        'sum_tonnage',
        'sum_exports',
        "price_per_barrel"
    })
    writer.writeheader()

    terre_mer = {}
    for row in rows_terremer:
      if row['partner'] not in terre_mer:
        terre_mer[row['partner']] = float(row['ratio_terre_mer'])

    toflit_exports_by_partner = {}
    for export in reader_toflit:
      partner = export['partner_simplification']
      if partner == "États-Unis d'Amérique":
        partner = 'Etats-Unis'
      value = float(export['value']) if export['value'] != '' else 0
      ratio_key = partner
      in_terre_mer = True
      if partner not in terre_mer:
        in_terre_mer = False
        # print('oups, no ratio for', partner)
        for r in terre_mer.keys():
          lower_case = r.lower()
          if partner.lower() in lower_case:
            ratio_key = r
            in_terre_mer = True
            # print(partner, ratio_key)
      if in_terre_mer:
        ratio = terre_mer[ratio_key]
        value = value * ratio
      
      # value = value * ratio
      if partner not in toflit_exports_by_partner:
        toflit_exports_by_partner[partner] = 0
      toflit_exports_by_partner[partner] += value
    navigo_exports_by_partner = {}
    for export in rows_navigo:
      partner = export['destination_partner_balance_1789']
      value = float(export['sum_tonnage']) if export['sum_tonnage'] != '' else 0
      if partner not in navigo_exports_by_partner:
        navigo_exports_by_partner[partner] = 0
      navigo_exports_by_partner[partner] += value
    print(toflit_exports_by_partner)
    for (partner, sum_tonnage) in navigo_exports_by_partner.items():
      # match = navigo_exports_by_partner[partner]
      if partner not in toflit_exports_by_partner:
        print('this partner is not in toflit: ' + partner)
      else:
        sum_exports = toflit_exports_by_partner[partner]
      writer.writerow({
        "partner": partner,
        "sum_tonnage": sum_tonnage,
        "sum_exports": sum_exports,
        "price_per_barrel": sum_exports / sum_tonnage
      })

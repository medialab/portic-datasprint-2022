import csv

# compteurs
total_exports_etranger = 0
total_exports_colonies = 0
total_exports_france = 0
total_total  = 0
number_of_flows_total = 0

# dictionnaire à deux niveaux bureaux -> partenaires (-> valeurs cumulées)
customs_offices = {}
partners = {}
# sélection des flows
selected_flows = []
# lecture du fichier (correspond à bdd_courante.csv.zip - https://github.com/medialab/toflit18_data/blob/master/base/bdd%20courante.csv.zip)
with open('../../../data/toflit18_all_flows.csv', newline='') as csvfile:
  flows = csv.DictReader(csvfile)
  # on itère dans chaque flux du csv
  # pour chaque flux ...
  for flow in flows:
    # on numérise la valeur du flux
    value = float(flow['value'] or 0)
    # on s'intéresse au flux si les 3 critères suivants sont remplis
    ie_type = flow['export_import'].lower()
    if flow['year'] == '1789' \
      and flow['customs_region'] == 'La Rochelle' \
      and flow['export_import'] == 'Exports':
        selected_flows.append(flow)
        # itération du compteur de valeur et nb de flux global
        total_total += value
        number_of_flows_total += 1
        # itération du compteur de valeur cumulée pour chaque type de partenaire
        if flow['partner_grouping'] == 'Amériques':
            total_exports_colonies += value
        elif flow['partner_grouping'] == 'France':
            total_exports_france += value
        else:
            total_exports_etranger += value

        # remplissage du dictionnaire des bureaux de ferme
        customs_office = flow['customs_office'] or "pas de bureau"
        if customs_office not in customs_offices:
            customs_offices[customs_office] = {
                "étranger": 0,
                "france": 0,
                "amériques": 0
            }
        partner_simp = flow['partner_grouping']
        if partner_simp not in partners:
          partners[partner_simp] = {
            'nb observations': 0,
            'valeur cumulée lt': 0
          }
        partners[partner_simp]['nb observations'] += 1
        partners[partner_simp]['valeur cumulée lt'] += value
        partner = "étranger"
        if flow['partner_grouping'] == 'France':
            partner = "france"
        elif flow['partner_grouping'] == 'Amériques':
            partner = "amériques"
        customs_offices[customs_office][partner] += value

################
## Dump flows ##
################

with open('./flows_la_rochelle_1789.csv', 'w') as outputfile:
  print('write csv')
  fieldnames = selected_flows[0].keys()
  writer = csv.DictWriter(outputfile, fieldnames)
  writer.writeheader()
  writer.writerows(selected_flows)
  print('done')

with open('./flows_la_rochelle_1789_by_partner.csv', 'w') as outputfile:
  print('write partners')
  partners_list = [{"partner_simplification": partner, **data} for partner, data in partners.items()]
  fieldnames = partners_list[0].keys()
  writer = csv.DictWriter(outputfile, fieldnames)
  writer.writeheader()
  writer.writerows(partners_list)
  print('done')


##########
## LOGS ##
##########
        
print("Nombre de flows total : ", number_of_flows_total)
print("Total total : ", f'{int(total_total):,}', 'lt')
print("Total exports de la direction des fermes de La Rochelle vers l'étranger (sans colonies et France) : ", f'{int(total_exports_etranger):,}', 'lt')
print("Total des exports de la direction des fermes de La Rochelle pour la France : ", f'{int(total_exports_france):,}', 'lt')
print("Total des exports de la direction des fermes de La Rochelle pour les Amériques : ", f'{int(total_exports_colonies):,}', 'lt')
print("Total exports étranger + France + Amériques : ", f'{int(total_exports_etranger + total_exports_france + total_exports_colonies):,}', 'lt')

print('bureau,partenaire,valeur lt')
for customs_office, partners in customs_offices.items():
    for partner, value in partners.items():
        print(customs_office + ',' + partner + ',' + str(int(value)))

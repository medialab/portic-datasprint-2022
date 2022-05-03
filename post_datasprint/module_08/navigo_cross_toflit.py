import csv

rows_navigo = []
rows_toflit = []

with open('../../productions/module_12/export_france_1787_par_pays_par_produits.csv', newline='') as csvfile:
    reader_navigo = csv.DictReader(csvfile)
    for row in reader_navigo:
        rows_navigo.append(row)

with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
    reader_toflit = csv.DictReader(csvfile)
    for row in reader_toflit:
        rows_toflit.append(row)

with open('navigo_cross_toflit.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames={
        'partner',
        'product',
        'value'
    })
    writer.writeheader()

    for row_navigo in rows_navigo:
        cross_toflit_lines = [
            row_toflit for row_toflit \
            in rows_toflit \
            if row_toflit['partner_simplification'] == row_navigo['destination_partner_balance_1789'] \
                and row_toflit['product_simplification'] == row_navigo['commodity_as_toflit']
        ]

        if len(cross_toflit_lines) > 0:
            value = sum([float(row_toflit['value'] or 0) for row_toflit in cross_toflit_lines])

            print(row_navigo['destination_partner_balance_1789'], row_navigo['commodity_as_toflit'])

            writer.writerow({
                'partner': row_navigo['destination_partner_balance_1789'],
                'product': row_navigo['commodity_as_toflit'],
                'value': value
            })
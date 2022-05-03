import csv

test = set()

fieldnames = {
    'year',
    'source_type',
    'export_import',
    # 'quantity',       not in database for these filters
    # 'quantity_unit',
    'value',
    'quantity_unit_simplification',
    'partner',
    'partner_simplification',
    'partner_grouping',
    'product',
    'product_orthographic',
    'product_simplification',
    'product_sitc_FR',
    'product_sitc_EN',
    'product_sitc_simplEN',
    'product_revolutionempire',
    'product_RE_aggregate',
    'product_reexportations'
}

with open('tolift_export_values_resume.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['source_type'] != 'Résumé':
                continue
            if row['year'] != '1787':
                continue
            if row['export_import'] != 'Exports':
                continue
            if row['partner_simplification'] != 'Angleterre':
                continue

            row = {key: value for key, value in row.items() if key in fieldnames}
            writer.writerow(row)
print(test)
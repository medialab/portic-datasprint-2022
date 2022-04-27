"""
description: https://github.com/medialab/portic-datasprint-2022/issues/3#issue-1184954966
"""

import csv

cust_rows = []
toflit_rows = []
product_rows = []

toflit_classification_used = 'product_simplification'
toflit_classification_required = set()
toflit_classification_memory = {}

cust_products = set()
toflit_products = set()

cust_fieldnames = {
    'dénomination partenaire',
    'dénomination produit niveau 1',
}
toflit_fieldnames = {
    'product_simplification',
    'partner_orthographic'
}

toflit_products_to_england = {}

for cust_source in ['cust-product-1789-england.csv', 'cust-product-1789-scotland.csv']:
    with open(cust_source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['type de flux'] == 'Exported':
                continue
            row = {key: value for key, value in row.items() if key in cust_fieldnames}
            row['destination'] = 'England' if cust_source == 'cust-product-1789-england.csv' else 'Scotland'
            cust_rows.append(row)
            cust_products.add(row['dénomination produit niveau 1'])

cust_fieldnames.add('destination')

with open('cust-1789.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=cust_fieldnames)
    writer.writeheader()
    for row in cust_rows:
        writer.writerow(row)

# Get CSV to translate CUST product with Toflit classification

with open('cust-1789-products.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames={'product-cust', 'product-toflit'})
    writer.writeheader()
    for product in cust_products:
        writer.writerow({
            'product-cust': product,
            'product-toflit': ''
        })

with open('cust-cross-toflit-products.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        product_rows.append(row)
        toflit_classification_required.add(row['product-toflit'])

with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['product_simplification'] in toflit_classification_required:
            toflit_classification_memory[row['product_simplification']] = row['product_simplification']

        if row['best_guess_region_prodxpart'] != '1':
            continue
        if row['year'] != '1789':
            continue
        if row['export_import'] != 'Exports':
            continue
        if row['partner_orthographic'] != 'Angleterre':
            continue
        
        toflit_products.add(row['product_simplification'])
        row = {key: value for key, value in row.items() if key in toflit_fieldnames}
        toflit_rows.append(row)

def trans_product_cust_to_toflit(cust_row):
    for trans_row in product_rows:
        if trans_row['product-cust'] == cust_row['dénomination produit niveau 1']:
            return trans_row['product-toflit']
    print('trans error for cust product ', cust_row['dénomination produit niveau 1'])

all_product = set(
    [toflit_product['product_simplification'] for toflit_product in toflit_rows] +
    [trans_product_cust_to_toflit(cust_product) for cust_product in cust_rows]
)

with open('cross-cust-toflit.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        'product',
        'toflit-exports',
        'cust-imports'
    ])
    writer.writeheader()

    toflit_products = {}
    cust_products = {}
    
    for toflit_row in toflit_rows:
        toflit_product = toflit_row['product_simplification']
        if toflit_product in toflit_products:
            toflit_products[toflit_product] += 1
        else:
            toflit_products[toflit_product] = 1
    
    for cust_row in cust_rows:
        cust_product = trans_product_cust_to_toflit(cust_row)
        if cust_product in cust_products:
            cust_products[cust_product] += 1
        else:
            cust_products[cust_product] = 1

    for product in all_product:
        writer.writerow({
            'product': product,
            'toflit-exports': toflit_products[product] if product in toflit_products else 0,
            'cust-imports': cust_products[product] if product in cust_products else 0
        })
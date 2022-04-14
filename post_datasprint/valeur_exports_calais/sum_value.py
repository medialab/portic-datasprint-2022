import csv

total = 0

products = {}

with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['best_guess_region_prodxpart'] != '1':
            continue
        if row['year'] != '1789':
            continue
        if row['export_import'] != 'Exports':
            continue
        if row['customs_office'] != 'Calais':
            continue

        row['value'] = float(row['value'] or 0)

        row_product = row['product_revolutionempire']

        if row_product in products:
            products[row_product]['occurence'] += 1
            products[row_product]['value'] += row['value']
        else:
            products[row_product] = {
                'occurence': 1,
                'value': row['value']
            }

print(products)

with open('products.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'product',
        'total_occurence',
        'total_value'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for product in products.keys():
        item = products[product]
        writer.writerow({
            'product': product,
            'total_occurence': item['occurence'],
            'total_value': item['value']
        })
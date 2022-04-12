import csv

CSV_FILE_INPUT_1787 = '../../data/navigo_all_flows_1787.csv'
CSV_FILE_INPUT_1789 = '../../data/navigo_all_flows_1789.csv'

products = {}

for source in [CSV_FILE_INPUT_1787]:

    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['destination_uhgs_id'] != 'A0394917':
                continue

            for product in [row['commodity_purpose'], row['commodity_purpose2'], row['commodity_purpose3'], row['commodity_purpose4']]:
                if product == '':
                    continue
                product = product.lower()
                if product in products:
                    products[product] += 1
                else:
                    products[product] = 1

with open('products_fake_destination.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'destination_uhgs_id',
        'product',
        'quantity'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for product in products.keys():
        quantity = products[product]
        writer.writerow({
            'destination_uhgs_id': 'A0394917',
            'product': product,
            'quantity': quantity
        })
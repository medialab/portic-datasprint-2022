import csv

toflit_products_simplification = set()

with open('../../data/toflit18_all_flows.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        toflit_products_simplification.add(row['product_simplification'])

with open('cust-cross-toflit-products.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['product-toflit'] not in toflit_products_simplification:
            print('product ' + row['product-toflit'] + ' is invalid')
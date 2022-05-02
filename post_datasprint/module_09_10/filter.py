import csv

DATA_P341 = 'donnees_pfister_p341_saisonnalite.csv'
DATA_P521 = 'donnees_pfister_p521_saisonnalite.csv'

rows = []

for source in [DATA_P341, DATA_P521]:

    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            row['year'] = int(row['year'])
            if row['year'] < 1787 or row['year'] > 1789:
                continue
            if 'direction' in row and row['direction'] == 'entrée'
                continue

            row['value'] = int(row['value']) if row['value'].isnumeric() == True else 0
            row['is_smoggleur'] = 1 if source == 'donnees_pfister_p341_saisonnalite.csv' else 0

            rows.append(row)

with open('values-month-year.csv', 'w', newline='') as csvfile:
    fieldnames = {
        'year',
        'month',
        'value',
        'is_smoggleur'
    }

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in rows:
        row = {key: value for key, value in row.items() if key in fieldnames}
        writer.writerow(row)
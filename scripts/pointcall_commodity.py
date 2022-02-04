import csv

fields = [
    'year',
    'flag',
    'ferme_bureau',
    'ferme_direction',
    'pointcall_province',
    'pointcall_admiralty',
    'pointcall_action',
    'commodity'
]

fields_commodity = [
    'commodity_purpose',
    'commodity_purpose2',
    'commodity_purpose3',
    'commodity_purpose4'
]

rows = []

CSV_FILE_OUTPUT = '../src/static/data/pointcall_commodity.csv'

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_pointcalls_' + year + '.csv'

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row_original in reader:
            # if row_original['pointcall'] != 'Dunkerque':
            #     continue

            row = dict.fromkeys(
                fields,
                '' # initial value for all fields
            )
            for commodity in fields_commodity:
                if row_original[commodity] == '':
                    continue

                for meta in row.keys():
                    if meta == 'year':
                        row[meta] = year
                        continue
                    if meta == 'commodity':
                        row[meta] = row_original[commodity]
                        continue
                    row[meta] = row_original[meta]
                rows.append(row)

with open(CSV_FILE_OUTPUT, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)
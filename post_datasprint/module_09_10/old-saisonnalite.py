import csv

years = {}
months = {}

with open('data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        row['value'] = int(row['value']) if row['value'].isnumeric() == True else 0
        
        if row['year'] in years:
            years[row['year']] += row['value']
        else:
            years[row['year']] = row['value']
        
        if row['month'] in months:
            months[row['month']] += row['value']
        else:
            months[row['month']] = row['value']

with open('years.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'year',
        'value'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for year in years.keys():
        value = years[year]
        writer.writerow({
            'year': year,
            'value': value
        })

with open('months.csv', 'w', newline='') as csvfile:
    fieldnames = [
        'month',
        'value'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for month in months.keys():
        value = months[month]
        writer.writerow({
            'month': month,
            'value': value
        })
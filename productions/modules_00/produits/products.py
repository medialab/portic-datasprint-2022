from mdutils.mdutils import MdUtils
import csv
import json

CSV_FILE_INPUT = 'liste_smoggleurs.csv'
JSON_FILE_OUTPUT = 'smoggleurs-product.json'

product = {}

with open(CSV_FILE_INPUT, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    fields = reader.fieldnames

    product = dict.fromkeys(
        reader.fieldnames,
        0
    )

    for row in reader:
        for field in fields:
            if row[field] != '':
                product[field] += 1

# Sort dict by value
product_sorted = {
    k: v for k, v in sorted(product.items(), key=lambda item: item[1])[::-1]
}

mdFile = MdUtils(file_name='product smoggleurs', title='Produits des smoggleurs')

mdFile.new_paragraph("À Dunkerque sur **868** sorties de smoggelurs connues en 1787 (2 manquants)")

mdFile.new_line("")
mdFile.new_line( "| Produit | Quantité |")
mdFile.new_line( "| --- | --- |")
for product in product_sorted:
    valeur = product_sorted[product]
    mdFile.new_line( "| " + product + " | " + str(valeur)  + " |")

mdFile.create_md_file()
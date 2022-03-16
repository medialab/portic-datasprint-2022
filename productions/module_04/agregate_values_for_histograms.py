#!/usr/bin/env python

import csv
import sys

CAT_PRODUCTS = sys.argv[1]
FILE_PATTERN = sys.argv[2]
SOURCES = sys.argv[3:5]
DESTINATIONS = sys.argv[5:7]

fulldata = {}

with open(CAT_PRODUCTS) as f:
    for row in csv.DictReader(f):
        if row["categorie"] not in fulldata:
            fulldata[row["categorie"]] = {
                "produits": [row["produit"]],
                "values": {dest: {source: 0 for source in SOURCES} for dest in DESTINATIONS}
            }
        else:
            fulldata[row["categorie"]]["produits"].append(row["produit"])

for source in SOURCES:
    for destination in DESTINATIONS:
        with open(FILE_PATTERN % (source, destination)) as f:
            for row in csv.DictReader(f):
                for cat in fulldata:
                    if row["product_revolutionempire"] in fulldata[cat]["produits"]:
                        fulldata[cat]["values"][destination][source] += float(row["value"] or 0)

writer = csv.writer(sys.stdout)
writer.writerow(["Série", "Destination", "Flows_from_%s" % SOURCES[0], "Flows_from_%s" % SOURCES[1]])
for cat in fulldata:
    for dest in DESTINATIONS:
        writer.writerow([cat, dest, fulldata[cat]["values"][dest][SOURCES[0]], fulldata[cat]["values"][dest][SOURCES[1]]])


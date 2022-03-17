#!/usr/bin/env python

import csv
import sys
from itertools import product

FILE_PATTERN = sys.argv[1]
SOURCES = sys.argv[2:4]
DESTINATIONS = sys.argv[4:6]

data = {}

unitproduct = lambda : {"%s_to_%s" % (s, d): 0 for (s, d) in product(SOURCES, DESTINATIONS)}

for source in SOURCES:
    for destination in DESTINATIONS:
        with open(FILE_PATTERN % (source, destination)) as f:
            for row in csv.DictReader(f):
                prod = row["product_revolutionempire"]
                if prod not in data:
                    data[prod] = unitproduct()
                data[prod]["%s_to_%s" % (source, destination)] += float(row["value"] or 0)

for prod in data:
    try:
        data[prod]["% Dunkerque / Ports Francs (from France)"] = 100 * data[prod]["france_to_dunkerque"] / (data[prod]["france_to_dunkerque"] + data[prod]["france_to_autres_portsfrancs"])
    except ZeroDivisionError:
        data[prod]["% Dunkerque / Ports Francs (from France)"] = ""
    try:
        data[prod]["% Dunkerque / Ports Francs (from étranger)"] = 100 * data[prod]["etranger_to_dunkerque"] / (data[prod]["etranger_to_dunkerque"] + data[prod]["etranger_to_autres_portsfrancs"])
    except ZeroDivisionError:
        data[prod]["% Dunkerque / Ports Francs (from étranger)"] = ""
    try:
        data[prod]["% Dunkerque / Ports Francs"] = 100 * (data[prod]["france_to_dunkerque"] + data[prod]["etranger_to_dunkerque"]) / (data[prod]["france_to_dunkerque"] + data[prod]["etranger_to_dunkerque"] + data[prod]["france_to_autres_portsfrancs"] + data[prod]["etranger_to_autres_portsfrancs"])
    except ZeroDivisionError:
        data[prod]["% Dunkerque / Ports Francs"] = ""

format_csv = lambda x: ("%.02f" % x).rstrip("0.") or "0" if x != "" else ""

writer = csv.writer(sys.stdout)
products = list(data.keys())
headers = sorted(list(data[products[0]].keys()))
writer.writerow(["produit"] + headers)
for prod in data:
    writer.writerow([prod] + [format_csv(data[prod][k]) for k in headers])


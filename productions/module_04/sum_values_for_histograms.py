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

totaux = {
    "Dunkerque": 0,
    "Dunkerque (from France)": 0,
    "Dunkerque (from étranger)": 0,
    "Autres Ports Francs": 0,
    "Autres Ports Francs (from France)": 0,
    "Autres Ports Francs (from étranger)": 0
}
for prod in data:
    totaux["Dunkerque"] += data[prod]["france_to_dunkerque"] + data[prod]["etranger_to_dunkerque"]
    totaux["Dunkerque (from France)"] += data[prod]["france_to_dunkerque"]
    totaux["Dunkerque (from étranger)"] += data[prod]["etranger_to_dunkerque"]
    totaux["Autres Ports Francs"] += data[prod]["france_to_autres_portsfrancs"] + data[prod]["etranger_to_autres_portsfrancs"]
    totaux["Autres Ports Francs (from France)"] += data[prod]["france_to_autres_portsfrancs"]
    totaux["Autres Ports Francs (from étranger)"] += data[prod]["etranger_to_autres_portsfrancs"]

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
    data[prod]["% / total Dunkerque"] = 100 * (data[prod]["france_to_dunkerque"] + data[prod]["etranger_to_dunkerque"]) / totaux["Dunkerque"]
    data[prod]["% / total Dunkerque (from France)"] = 100 * data[prod]["france_to_dunkerque"] / totaux["Dunkerque (from France)"]
    data[prod]["% / total Dunkerque (from étranger)"] = 100 * data[prod]["etranger_to_dunkerque"] / totaux["Dunkerque (from étranger)"]
    data[prod]["% / total Autres Ports Francs"] = 100 * (data[prod]["france_to_autres_portsfrancs"] + data[prod]["etranger_to_autres_portsfrancs"]) / totaux["Autres Ports Francs"]
    data[prod]["% / total Autres Ports Francs (from France)"] = 100 * data[prod]["france_to_autres_portsfrancs"] / totaux["Autres Ports Francs (from France)"]
    data[prod]["% / total Autres Ports Francs (from étranger)"] = 100 * data[prod]["etranger_to_autres_portsfrancs"] / totaux["Autres Ports Francs (from étranger)"]


format_csv = lambda x: ("%.02f" % x).rstrip("0.") or "0" if x != "" else ""

writer = csv.writer(sys.stdout)
products = list(data.keys())
headers = sorted(list(data[products[0]].keys()))
writer.writerow(["produit"] + headers)
for prod in data:
    writer.writerow([prod] + [format_csv(data[prod][k]) for k in headers])

for source in SOURCES:
    for dest in DESTINATIONS:
        with open("top20_%s_to_%s.csv" % (source, dest), "w") as f:
            writer = csv.writer(f)
            writer.writerow(["produit", "%s_to_%s" % (source, dest)])
            prods = [(prod, data[prod]["%s_to_%s" % (source, dest)]) for prod in data.keys()]
            top20 = sorted(prods, key=lambda a: a[1], reverse=True)[:20]
            for row in top20:
                writer.writerow(row)
            prop = sum([a[1] for a in top20[:10]]) / sum([a[1] for a in prods]) * 100
            print("Le top 10 des produits importés depuis %s vers %s représente %.02f%%" % (source, dest, prop), file=sys.stderr)
for typ in ["", " (from France)", " (from étranger)"]:
    typ_ = typ.replace(" ", "_").replace("(", "").replace(")", "")
    with open("top20_%%_dunkerque_sur_portsfrancs%s.csv" % typ_, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["produit", "%%_dunkerque_sur_portsfrancs%s.csv" % typ_])
        prods = [(prod, data[prod]["%% Dunkerque / Ports Francs%s" % typ]) for prod in data.keys() if data[prod]["%% Dunkerque / Ports Francs%s" % typ]]
        top20 = sorted(prods, key=lambda a: a[1], reverse=True)[:20]
        for row in top20:
            writer.writerow(row)
    with open("top20_%%_sur_total_dunkerque%s.csv" % typ_, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["produit", "%%_sur_total_dunkerque%s.csv" % typ_])
        prods = [(prod, data[prod]["%% / total Dunkerque%s" % typ]) for prod in data.keys() if data[prod]["%% / total Dunkerque%s" % typ]]
        top20 = sorted(prods, key=lambda a: a[1], reverse=True)[:20]
        for row in top20:
            writer.writerow(row)
    with open("top20_%%_sur_total_autres_portsfrancs%s.csv" % typ_, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["produit", "%%_sur_total_autres_portsfrancs%s.csv" % typ_])
        prods = [(prod, data[prod]["%% / total Autres Ports Francs%s" % typ]) for prod in data.keys() if data[prod]["%% / total Autres Ports Francs%s" % typ]]
        top20 = sorted(prods, key=lambda a: a[1], reverse=True)[:20]
        for row in top20:
            writer.writerow(row)

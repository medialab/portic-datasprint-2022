import csv
import json
from collections import defaultdict
import sys

file = "../../../data/toflit18_all_flows.csv"

autres_port_francs = [
    "Lorient",
    "Bayonne",
    "Marseille",
]
dunkerque_port_franc = "Dunkerque"


def import_partner_class(partner):
    if partner in ["Asie", "Afrique", "Amériques"]:
        return "colonies"
    if partner == "France":
        return "France"
    return "Monde"


# Product type definition
product_factories = {
    "colonial_others": lambda row: "colonial"
    if import_partner_class(row["partner_grouping"]) == "colonies"
    else "other",
    "colonial_products": lambda row: row["product_revolutionempire"],
}


detail_products_trade = {
    p: defaultdict(lambda: defaultdict(dict))
    for p in autres_port_francs + [dunkerque_port_franc]
}
total_trade = {
    p: defaultdict(lambda: defaultdict(dict))
    for p in autres_port_francs + [dunkerque_port_franc]
}
colonial_products_other_ports = {
    p: set() for p in autres_port_francs + [dunkerque_port_franc]
}

sources = set()
partners_anom = set()

# file = toflit18 all flows
with open(file, "r") as muerte:
    reader = csv.DictReader(muerte)
    # @todo filter by source type to be clean ? ("best_guess_region_prodxpart" ?)
    for i, row in enumerate(reader):

        if row["year"] == "1789":
            value = float(row["value"]) if row["value"] else 0.0
            office = (
                row["customs_office"]
                if row["customs_office"] != "Port franc de Bayonne et Saint Jean de Luz"
                else "Bayonne"
            )

            product = row["product_revolutionempire"]
            partner_type = import_partner_class(row["partner_grouping"])

            # trade reporting by Dunkerque port franc
            if office == dunkerque_port_franc:
                if row["export_import"] == "Exports":
                    if partner_type != "colonies":
                        # export in Dunkerque are necessarly colonial products
                        # detail prodcuts only depicts colonial products for Dunkerque
                        detail_products_trade[office][product][partner_type][
                            row["export_import"]
                        ] = (
                            detail_products_trade[office][product][partner_type].get(
                                row["export_import"], 0
                            )
                            + value
                        )
                    export_type_total = (
                        "produits coloniaux"
                        if partner_type != "colonies"
                        else "autres produits"
                    )

                    total_trade[office][export_type_total][partner_type][
                        row["export_import"]
                    ] = (
                        total_trade[office][export_type_total][partner_type].get(
                            row["export_import"], 0
                        )
                        + value
                    )
                    if partner_type == "France":
                        print(
                            "destination France dans export produits coloniaux Dunkerque"
                        )
                elif row["export_import"] == "Imports":
                    product_type = "autres produits"
                    if partner_type == "colonies":
                        colonial_products_other_ports[office].add(product)
                        detail_products_trade[office][product][partner_type][
                            row["export_import"]
                        ] = (
                            detail_products_trade[office][product][partner_type].get(
                                row["export_import"], 0
                            )
                            + value
                        )
                        product_type = "produits coloniaux"
                    total_trade[office][product_type][partner_type][
                        row["export_import"]
                    ] = (
                        total_trade[office][product_type][partner_type].get(
                            row["export_import"], 0
                        )
                        + value
                    )
            # trade reported by other ports francs
            elif office in autres_port_francs:
                if row["export_import"] == "Exports":

                    detail_products_trade[office][product][partner_type][
                        row["export_import"]
                    ] = (
                        detail_products_trade[office][product][partner_type].get(
                            row["export_import"], 0
                        )
                        + value
                    )
                elif row["export_import"] == "Imports":
                    detail_products_trade[office][product][partner_type][
                        row["export_import"]
                    ] = (
                        detail_products_trade[office][product][partner_type].get(
                            row["export_import"], 0
                        )
                        + value
                    )
                    if partner_type == "colonies":
                        colonial_products_other_ports[office].add(product)
                # store total trade by partner type
                # we can isolate produits coloniaux thanks to the specific source + partner
                type_produit = "autres produits"

                # ANOM gives colonial products re-exports partner = "Monde hors colonies" for Dunkerque, Marseille and Lorient but not for Bayonne
                if (
                    (
                        row["partner_simplification"] == "Monde hors colonies"
                        # using a fixed list of products instead for Bayonne = product which imports value are at least 50% from colonies
                        or (office == "Bayonne" and product in ["Sucre", "Café"])
                    )
                    and row["export_import"] == "Exports"
                ) or (row["export_import"] == "Imports" and partner_type == "colonies"):

                    type_produit = "produits coloniaux"
                total_trade[office][type_produit][partner_type][
                    row["export_import"]
                ] = (
                    total_trade[office][type_produit][partner_type].get(
                        row["export_import"], 0
                    )
                    + value
                )
            else:
                # process mirror flows : France imports from Dunkerque or Bayonne
                if row["partner_simplification"] == "Dunkerque":

                    if product:
                        total_trade["Dunkerque"]["autres produits"]["France"][
                            row["export_import"]
                        ] = (
                            total_trade["Dunkerque"]["autres produits"]["France"].get(
                                row["export_import"], 0
                            )
                            + value
                        )
                        # NOTE: we desactivate to complement detail product with miror flows as there a no colonial products in there
                        # deatil_products_trade["Dunkerque"][product]["France"][
                        #     row["export_import"]
                        # ] = (
                        #     deatil_products_trade["Dunkerque"][product]["France"].get(
                        #         row["export_import"], 0
                        #     )
                        #     + value
                        # )
                if row["partner_simplification"] in ["Bayonne", "Saint-Jean de Luz"]:

                    if product:
                        total_trade["Bayonne"]["autres produits"]["France"][
                            row["export_import"]
                        ] = (
                            total_trade["Bayonne"]["autres produits"]["France"].get(
                                row["export_import"], 0
                            )
                            + value
                        )
                        detail_products_trade["Bayonne"][product]["France"][
                            row["export_import"]
                        ] = (
                            detail_products_trade["Bayonne"][product]["France"].get(
                                row["export_import"], 0
                            )
                            + value
                        )

    export_data = {
        p: {"detail_products": [], "total_trade": []}
        for p in autres_port_francs + [dunkerque_port_franc]
    }
    total_Dunkerque_export_colonial_to_France = 0
    for (port, colional_products) in detail_products_trade.items():
        for product, product_trade in colional_products.items():
            # filter deatil product to keep only colonial products for Dunkerque
            # NOTE: this filter is deprecated as we desactivated to complement ANOM products with mirors flows in detail product
            if port != "Dunkerque" or product in colonial_products_other_ports[port]:
                totals = defaultdict(int)
                for (partner_type, values) in product_trade.items():
                    for impexp, value in values.items():
                        export_data[port]["detail_products"].append(
                            {
                                "product": product,
                                "value": value,
                                "importsexports": impexp,
                                "partner_type": partner_type,
                                "port": port,
                            }
                        )
                        totals[impexp] += value
                        if (
                            port == "Dunkerque"
                            and impexp == "Exports"
                            and partner_type == "France"
                        ):
                            total_Dunkerque_export_colonial_to_France += value

                export_data[port]["detail_products"].append(
                    {
                        "product": product,
                        "value": totals["Imports"] - totals["Exports"]
                        if totals["Exports"] < totals["Imports"]
                        else totals["Exports"] - totals["Imports"],
                        "importsexports": "Exports"
                        if totals["Exports"] < totals["Imports"]
                        else "Imports",
                        "partner_type": "Fraude ?",
                        "port": port,
                    }
                )
    # NOTE: commented as mirors flows are only considered as no colonial products
    # substract colonial product from Dunkerque export Autre Produits to France
    # print(
    #     f"subtract colonial from Dunkerque exoirt Autre profuits: {total_Dunkerque_export_colonial_to_France}"
    # )
    # total_trade["Dunkerque"]["produits coloniaux"]["France"][
    #     "Exports"
    # ] = total_Dunkerque_export_colonial_to_France
    total_trade["Dunkerque"]["autres produits"]["France"]["Exports"] = (
        total_trade["Dunkerque"]["autres produits"]["France"]["Exports"]
        - total_Dunkerque_export_colonial_to_France
    )

    for (port, totals) in total_trade.items():

        for (product_type, partner_types) in totals.items():
            totals = defaultdict(int)
            for partner_type, values in partner_types.items():
                for impexp, value in values.items():
                    export_data[port]["total_trade"].append(
                        {
                            "port": port,
                            "product_type": product_type,
                            "partner_type": partner_type,
                            "importsexports": impexp,
                            "value": value,
                        }
                    )
                    totals[impexp] += value

            export_data[port]["total_trade"].append(
                {
                    "port": port,
                    "product_type": product_type,
                    "value": totals["Imports"] - totals["Exports"]
                    if totals["Exports"] < totals["Imports"]
                    else totals["Exports"] - totals["Imports"],
                    "importsexports": "Exports"
                    if totals["Exports"] < totals["Imports"]
                    else "Imports",
                    "partner_type": "Fraude ?",
                }
            )

    with open("data/import_export_ports_francs.json", "w") as f:
        json.dump(export_data, f, indent=2)

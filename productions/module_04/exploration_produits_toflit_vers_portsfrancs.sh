#!/bin/bash

cd $(dirname $0)/../../data/

mkdir -p module_04
cd module_04
rm -f toflit18*
ln -s ../toflit18_all_flows.csv toflit18_all_flows.csv

xsv search Dunkerque -s partner_simplification toflit18_all_flows.csv | xsv search Exports -s export_import > toflit18_flows_france_to_dunkerque.csv
xsv search Dunkerque -s customs_office toflit18_all_flows.csv | xsv search Imports -s export_import > toflit18_flows_etranger_to_dunkerque.csv
xsv search "178[79]" -s year toflit18_flows_france_to_dunkerque.csv | xsv select product_revolutionempire | xsv frequency -l 0 | sed 's/,value,count/,produit,count_france_to_dunkerque/' | xsv select 2- > toflit18_products_france_to_dunkerque_1787-1789.csv
xsv search "178[79]" -s year toflit18_flows_etranger_to_dunkerque.csv | xsv select product_revolutionempire | xsv frequency -l 0 | sed 's/,value,count/,produit,count_etranger_to_dunkerque/' | xsv select 2- > toflit18_products_etranger_to_dunkerque_1787-1789.csv

xsv search -i "Bayonne|Lorient|Marseille|Noirmoutier|Yeu|Bouin" -s partner_simplification toflit18_all_flows.csv | xsv search -iv "Dunkerque" -s partner_simplification | xsv search Exports -s export_import > toflit18_flows_france_to_autres_portsfrancs.csv
xsv search -i "Bayonne|Lorient|Marseille|Noirmoutier|Yeu|Bouin" -s customs_office toflit18_all_flows.csv | xsv search -iv "Saint-Esprit de Bayonne" -s customs_office | xsv search Imports -s export_import > toflit18_flows_etranger_to_autres_portsfrancs.csv
xsv search "178[79]" -s year toflit18_flows_france_to_autres_portsfrancs.csv | xsv select product_revolutionempire | xsv frequency -l 0 | sed 's/,value,count/,produit,count_france_to_autres_portsfrancs/' | xsv select 2- > toflit18_products_france_to_autres_portsfrancs_1787-1789.csv
xsv search "178[79]" -s year toflit18_flows_etranger_to_autres_portsfrancs.csv | xsv select product_revolutionempire | xsv frequency -l 0 | sed 's/,value,count/,produit,count_etranger_to_autres_portsfrancs/' | xsv select 2- > toflit18_products_etranger_to_autres_portsfrancs_1787-1789.csv

xsv join --left produit ../produits_smoggles_typiques.csv produit toflit18_products_france_to_dunkerque_1787-1789.csv | xsv select 1,2,4 > /tmp/join1.csv
xsv join --left produit /tmp/join1.csv produit toflit18_products_etranger_to_dunkerque_1787-1789.csv | xsv select 1,2,3,5 > /tmp/join2.csv
xsv join --left produit /tmp/join2.csv produit toflit18_products_france_to_autres_portsfrancs_1787-1789.csv | xsv select 1,2,3,4,6 > /tmp/join3.csv
xsv join --left produit /tmp/join3.csv produit toflit18_products_etranger_to_autres_portsfrancs_1787-1789.csv | xsv select 1,2,3,4,5,7 > produits_smoggles_typiques_france-etranger_to_dunkerque-autres_portsfrancs.csv


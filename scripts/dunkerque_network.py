import csv
import networkx as nx
import json

Graph = nx.Graph()
destinations_from_dunkerque = {}

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_flows_' + year + '.csv'

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['departure'].lower() != 'dunkerque':
                continue

            if row['destination'] in destinations_from_dunkerque:
                destinations_from_dunkerque[row['destination']]['tonnage'] += int(row['tonnage']) if row['tonnage'].isnumeric() == True else 0
            else:
                destinations_from_dunkerque[row['destination']] = {
                    'tonnage' : 0,
                    'pays' : row['flag']
                }

for destination in destinations_from_dunkerque.keys():
    metas = destinations_from_dunkerque[destination]

    Graph.add_nodes_from([
        (destination, metas)
    ])

destinations_from_dunkerque_list = list(destinations_from_dunkerque)

for year in ['1787', '1789']:
    CSV_FILE_INPUT = '../data/navigo_all_flows_' + year + '.csv'

    with open(CSV_FILE_INPUT, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['destination'] in destinations_from_dunkerque_list and row['departure'] in destinations_from_dunkerque_list:
                Graph.add_edge(row['departure'], row['destination'])

print(
    
)

with open('../../src/static/data/destinations_from_dunkerque.json', 'w', encoding='utf-8') as f:
    json.dump(
        nx.readwrite.json_graph.node_link_data(Graph),
        f,
        ensure_ascii=False,
        indent=4
    )
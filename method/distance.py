import networkx as nx
# import pandas as pd
import json

graph = {
    'G1': {'C101': 1, 'SAC': 1},
    'C101': {'G1': 1, 'C102': 1},
    'C102': {'C101': 1, 'C102P': 1},
    'C102P': {'C102': 1, 'C103': 1},
    'C103': {'C102P': 1, 'C104': 1},
    'C104': {'C103': 1, 'C105': 1},
    'C105': {'C104': 1, 'C105P': 1},
    'C105P': {'C105': 1, 'TE': 1},
    'TE': {'C105P': 1, 'E105': 1},
    'E105': {'TE': 1, 'E106': 1},
    'E106': {'E105': 1, 'E107': 1},
    'E107': {'E106': 1, 'E108': 1},
    'E108': {'E107': 1, 'CED': 1},
    'CED': {'E108': 1, 'D104': 1},
    'D104': {'CED': 1, 'D103': 1},
    'D103': {'D104': 1, 'D102': 1},
    'D102': {'D103': 1, 'A101': 1},
    'A101': {'D102': 1, 'G2': 1},
    'G2': {'A101': 1, 'A102': 1},
    'A102': {'G2': 1, 'SAC': 1},
    'SAC': {'A102': 1, 'G1': 1},
}

# dir_data = "C:/Users/dismo/OneDrive/Documents/Alfian Prisma Yopiangga/Bangkit/Capstone/code/flask-api-mata/dataset/data-d4-l1-v2.csv"
dir_data = "/var/www/flask-api-mata/dataset/data-d4-l1-v2.csv"

with open(dir_data, 'r') as file:
    data = json.load(file)
data = data['data']

G = nx.Graph()
G.add_nodes_from(graph.keys())
for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)

def get_distance(source, target):
    path = nx.dijkstra_path(G, source, target)

    data_path = []
    
    for i in range(len(path)-1):
        for j in range(len(data)):
            if data[j]['id'] == path[i]:
                data_path.append(data[j])
                break

    return data_path


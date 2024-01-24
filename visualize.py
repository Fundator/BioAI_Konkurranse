import matplotlib.pyplot as plt
from typing import List
import numpy as np

def visualize(route: List[int], task: int, round_trip: bool):

    try:
        import networkx as nx
    except ModuleNotFoundError or ImportError:
        print('pip install networkx dersom du ønsker å visualisere den beste reiseruten')
        return

    tasks = ["vanskelig", "veldig_vanskelig"]
    destinations = list(np.loadtxt(f'BioAI_Konkurranse/data/xy/{tasks[task - 3]}.txt'))

    n_destinations = len(destinations)

    destinations = list(map(tuple, destinations))
    destination_nodes = [(xy, {"color": 'r', "pos": xy}) for xy in destinations]

    G = nx.Graph()
    G.add_nodes_from(destination_nodes)

    for i in range(0, len(route) - 1):
        G.add_edge(destinations[route[i]], destinations[route[i + 1]])
    if round_trip:
        G.add_edge(destinations[route[-1]], destinations[route[0]])


    pos = nx.get_node_attributes(G, 'pos')
    node_color = "red" if not round_trip else ["red"] + ["blue" for _ in range(n_destinations - 2)] + ["red"]
    size = 75 if not round_trip else [100] + [75 for _ in range(n_destinations - 2)] + [100]
    
    nx.draw(G, pos, node_color=node_color,  node_size=size)
    
    plt.gcf()
    plt.show()
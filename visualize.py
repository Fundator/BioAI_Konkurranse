import matplotlib.pyplot as plt
from typing import List
import numpy as np
import random

def visualize(route: List[int], task: int):

    try:
        import networkx as nx
    except ModuleNotFoundError or ImportError:
        print('pip install networkx dersom du ønsker å visualisere den beste reiseruten')
        return

    tasks = ["vanskelig", "veldig_vanskelig"]
    destinations = list(np.loadtxt(f'data/xy/{tasks[task - 3]}.txt'))

    destinations = list(map(tuple, destinations))
    destination_nodes = [(xy, {"color": 'r', "pos": xy}) for xy in destinations]

    G = nx.Graph()
    G.add_nodes_from(destination_nodes)

    for i in range(0, len(route) - 1):
        G.add_edge(destinations[route[i]], destinations[route[i + 1]])
    G.add_edge(destinations[route[-1]], destinations[route[0]])


    pos = nx.get_node_attributes(G, 'pos')
    node_color = "red"
    size = 75
    
    nx.draw(G, pos, node_color=node_color,  node_size=size)
    
    plt.gcf()
    plt.show()
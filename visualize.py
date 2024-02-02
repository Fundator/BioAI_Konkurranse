import matplotlib.pyplot as plt
from typing import List
import numpy as np

def visualize(route: List[int], task: int, round_trip: bool = True, file_name: str = "", invert_board: bool = False):

    try:
        import networkx as nx
    except ModuleNotFoundError or ImportError:
        print('pip install networkx dersom du ønsker å visualisere den beste reiseruten')
        return

    tasks = ["lett", "vanskelig", "veldig_vanskelig", "abakus_bedpres"]
    file_name = file_name if file_name != "" else f"{tasks[task] - 1}.txt"


    positions = np.loadtxt(f'BioAI_Konkurranse/data/xy/{file_name}')
    if invert_board:
        positions[:, 1] = -positions[:, 1]

    n_destinations = len(positions)

    positions = list(map(tuple, list(positions)))

    destination_nodes = [(positions[dest], {"color": 'r', "pos": positions[dest]}) for dest in route]

    G = nx.Graph()
    G.add_nodes_from(destination_nodes)

    for i in range(0, len(route) - 1):
        G.add_edge(positions[route[i]], positions[route[i + 1]])
    if round_trip:
        G.add_edge(positions[route[-1]], positions[route[0]])


    pos = nx.get_node_attributes(G, 'pos')
    node_color = "red" if round_trip else ["red"] + ["blue" for _ in range(n_destinations - 2)] + ["red"]
    size = 75 if round_trip else [100] + [75 for _ in range(n_destinations - 2)] + [100]
    
    nx.draw(G, pos, node_color=node_color,  node_size=size)
    
    plt.gcf()
    plt.show()
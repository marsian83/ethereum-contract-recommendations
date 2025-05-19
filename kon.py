import networkx as nx
import matplotlib.pyplot as plt
import random

total_nodes = 100
user_ratio = 0.75  
num_users = int(total_nodes * user_ratio)
num_contracts = total_nodes - num_users

G = nx.gnm_random_graph(n=total_nodes, m=300)  # m = number of edges

node_types = {}
for i, node in enumerate(G.nodes()):
    node_types[node] = 'user' if i < num_users else 'contract'

nodes = list(G.nodes())
random.shuffle(nodes)
for i, node in enumerate(nodes):
    node_types[node] = 'user' if i < num_users else 'contract'

color_map = ['red' if node_types[node] == 'user' else 'blue' for node in G.nodes()]

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, seed=42) 

nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=100)
nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3, width=0.8)
plt.axis('off')
plt.title(" Transaction Graph (Red=Users, Blue=Contracts)")
plt.show()

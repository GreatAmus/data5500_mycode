'''
Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph.
'''

import networkx as nx

# This first function uses the built in "number of nodes" function built into networkx
def node_count_easy(g):
    return g.number_of_nodes()

# This second function uses a length function to get the number of nodes in the graph
def node_count_manual(g):
    return len(g.nodes())

# Create a graph
g = nx.Graph()
g.add_edges_from([(1,2), (1,3), (3,5), (4,5)])

# print the nodes and edges
print("Number of nodes - using networkx:",node_count_easy(g))
print("Number of nodes - using manual:",node_count_manual(g))
print("Edges", g.number_of_edges())


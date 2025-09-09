'''
  2. Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph that have a degree greater than 5
  Chat history: https://chatgpt.com/share/68c06953-f9a4-8010-bf15-08acc7bd7d96
'''

import networkx as nx

# get the degrees greater than 5
def degree_greater_than_5(g):

    # I asked chat GPT to simplify the code I had here before. I did not know __ was considered a throw-away iterator
    # Also, the tuple return for the loop is super interesting 
    return sum(1 for __, deg in g.degree if deg > 5)
    
# create the graph
g = nx.Graph()
g.add_edges_from([(1,2), (1,3), (3,5), (4,5), (3,8), (3,6), (3,9), (3, 10), (1,4), (1,10), (1,8), (1,9)])

# print the number of nodes with a degree > 5
print("Number of nodes with degree > 5:",degree_greater_than_5(g))

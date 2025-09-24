import networkx as nx
import json
import requests
import math
from PathCollection import *
from CryptoPrinter import *

class CryptoGraph:

    def __init__(self, coins: dict[str, str]):
        self.__coins = coins
        self.__graph = nx.DiGraph()
        self.__all_paths = PathCollection()

    @property
    def coins(self):
        return self.__coins
    
    @property
    def graph(self) -> nx.DiGraph:
        return self.__graph
    
    @property
    def all_paths(self) -> "PathCollection":
        return self.__all_paths

    def get_prices(self):
        coin_names = ','.join(self.coins.keys())
        coin_symbols = ','.join(self.coins.values())

        url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_names}&vs_currencies={coin_symbols}'
        data = requests.get(url).json()
        return data

    def create_graph(self, data):
        for coin_id, quote in data.items():
            v1 = self.coins[coin_id]
            for v2, weight in quote.items():
                if v1 != v2 and weight is not None:
                    self.graph.add_edge(v1, v2, weight=weight)

    def get_weight(self, path):
        try:
            return math.prod(self.graph[v1][v2]['weight'] for v1, v2 in zip(path, path[1:]))
        except KeyError:
            return None

    def analytics(self):
        for v1, v2 in self.graph.edges():
            if v1 != v2:
                key = f'{v1} to {v2}'
                p = []    
                for path in nx.all_simple_paths(self.graph, v1, v2):
                    rev = path[::-1]
                    new_path = PathData(path, rev, self.get_weight(path), self.get_weight(rev))       
                    p.append(new_path)
                self.all_paths.add_path(key, p)

    def print_data(self):
        CryptoPrinter().print_data(self.all_paths)

    def export_data(self, filename):
        CryptoPrinter().export_data(filename, self.all_paths)
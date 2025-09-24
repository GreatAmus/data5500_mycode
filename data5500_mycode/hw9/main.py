
from CryptoGraph import *

coins = {'ripple': 'xrp', 
    'cardano': 'ada', 
    'bitcoin-cash':'bch', 
    'eos': 'eos', 
    'litecoin': 'ltc', 
    'ethereum': 'eth', 
    'bitcoin': 'btc'}

graph = CryptoGraph(coins)
graph.create_graph(graph.get_prices())
graph.analytics()
graph.print_data()
graph.export_data('data_trade')

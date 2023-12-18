import osmnx as ox
city = 'Russia, Saint Petersburg'
filepath = '../data/drive_graph'

G = ox.graph_from_place(city, network_type='drive')
# ox.plot_graph(G)
ox.save_graphml(G, filepath)

G = ox.load_graphml(filepath)

a = 2

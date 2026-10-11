
import osmnx as ox
import networkx as nx
from pathlib import Path

graph_path = Path("data/raw/delhi_walk_network.graphml")

G = ox.load_graphml(graph_path)

print("Saved network loaded successfully!")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print("Connected components:", nx.number_weakly_connected_components(G))

# Calculate basic road-network statistics
edge_lengths = [
    data["length"]
    for _, _, data in G.edges(data=True)
    if "length" in data
]

print("\n--- Road Network Statistics ---")
print(f"Total road segments: {len(edge_lengths)}")
print(f"Total network length: {sum(edge_lengths) / 1000:.2f} km")
print(f"Average segment length: {sum(edge_lengths) / len(edge_lengths):.2f} metres")
print(f"Longest segment: {max(edge_lengths):.2f} metres")

# Find the network node nearest to IIT Delhi
iitd_latitude = 28.5450
iitd_longitude = 77.1926

nearest_node = ox.distance.nearest_nodes(
    G,
    X=iitd_longitude,
    Y=iitd_latitude,
)

node_data = G.nodes[nearest_node]

print("\n--- IIT Delhi Reference Node ---")
print("Nearest node ID:", nearest_node)
print("Latitude:", node_data["y"])
print("Longitude:", node_data["x"])

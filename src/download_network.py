
import osmnx as ox
from pathlib import Path
import networkx as nx

# Create the directory for downloaded data
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

# Approximate centre of IIT Delhi
latitude = 28.5450
longitude = 77.1926

# Download a larger network to reduce boundary effects
network_radius = 3000

print("UrbanReach: Downloading expanded walking network...")

G = ox.graph_from_point(
    (latitude, longitude),
    dist=network_radius,
    network_type="walk",
    simplify=True,
)

print("Download successful!")
print("Nodes:", len(G.nodes))
print("Edges:", len(G.edges))

# Save the graph for future analysis
graph_path = output_dir / "delhi_walk_network.graphml"
ox.save_graphml(G, filepath=graph_path)

# Export GIS layers for QGIS
nodes, edges = ox.graph_to_gdfs(G)

nodes.to_file(
    output_dir / "road_nodes.geojson",
    driver="GeoJSON",
)

edges.to_file(
    output_dir / "road_edges.geojson",
    driver="GeoJSON",
)

print("\nExpanded network saved successfully!")
print("Graph:", graph_path)
print("Node layer:", output_dir / "road_nodes.geojson")
print("Edge layer:", output_dir / "road_edges.geojson")

print("\n--- Network Connectivity Check ---")
print("Is the graph strongly connected:", nx.is_strongly_connected(G))
print("Number of connected components:", nx.number_weakly_connected_components(G))

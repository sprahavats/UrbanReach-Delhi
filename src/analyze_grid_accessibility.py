import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Load the walking network
graph_path = Path("data/raw/delhi_walk_network.graphml")
G = ox.load_graphml(graph_path)

# Load the analysis grid and healthcare facilities
grid = gpd.read_file("data/processed/analysis_grid.geojson")
services = gpd.read_file("data/raw/healthcare_services.geojson")

# Keep grid coordinates in latitude/longitude for network-node lookup
grid = grid.to_crs("EPSG:4326")

# Calculate representative points in a projected CRS
# before converting them to latitude/longitude
services = services.to_crs("EPSG:32643")
services["geometry"] = services.geometry.representative_point()
services = services.to_crs("EPSG:4326")

# Find the nearest road-network node for every grid point
grid_nodes = ox.distance.nearest_nodes(
    G,
    X=grid.geometry.x,
    Y=grid.geometry.y
)

# Find the nearest road-network node for every healthcare facility
service_nodes = ox.distance.nearest_nodes(
    G,
    X=services.geometry.x,
    Y=services.geometry.y
)

# Calculate the shortest walking-network distance
# from every grid point to every healthcare facility
results = []

for index, grid_node in enumerate(grid_nodes):
    shortest_distances = nx.single_source_dijkstra_path_length(
        G,
        source=grid_node,
        weight="length"
    )

    reachable_services = [
        (service_index, shortest_distances[node])
        for service_index, node in enumerate(service_nodes)
        if node in shortest_distances
    ]

    if reachable_services:
        nearest_service_index, distance_metres = min(
            reachable_services,
            key=lambda item: item[1]
        )

        results.append({
            "grid_id": int(grid.iloc[index]["grid_id"]),
            "nearest_service": str(
                services.iloc[nearest_service_index].get("name", "Unnamed")
            ),
            "network_distance_m": round(distance_metres, 2),
            "network_distance_km": round(distance_metres / 1000, 3)
        })
    else:
        results.append({
            "grid_id": int(grid.iloc[index]["grid_id"]),
            "nearest_service": None,
            "network_distance_m": None,
            "network_distance_km": None
        })

# Save the results
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "grid_healthcare_accessibility.csv"
pd.DataFrame(results).to_csv(output_path, index=False)

print("Grid healthcare accessibility analysis complete!")
print("Grid points analysed:", len(results))
print("Reachable grid points:", sum(
    row["network_distance_m"] is not None for row in results
))
print("Average nearest-service distance (km):",
      round(pd.DataFrame(results)["network_distance_km"].mean(), 3))
print("Results saved to:", output_path)

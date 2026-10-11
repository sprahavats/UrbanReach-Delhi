
import networkx as nx
import osmnx as ox
import pandas as pd
import geopandas as gpd
from pathlib import Path

# Load saved data
G = ox.load_graphml("data/raw/delhi_walk_network.graphml")
services = gpd.read_file("data/raw/healthcare_services.geojson")
reference = pd.read_csv("data/reference_points.csv")

reference_node = int(reference.loc[0, "node_id"])

print("Calculating walking-network distances...")

results = []

for _, service in services.iterrows():
    # Use a representative point for both points and polygons
    point = service.geometry.representative_point()

    # Find the nearest walking-network node
    service_node = ox.distance.nearest_nodes(
        G,
        X=point.x,
        Y=point.y,
    )

    # Calculate shortest walking distance in metres
    distance = nx.shortest_path_length(
        G,
        source=reference_node,
        target=service_node,
        weight="length",
    )

    results.append({
        "name": service.get("name"),
        "amenity": service.get("amenity"),
        "network_distance_km": distance / 1000,
        "service_node": service_node,
    })

# Save results
results_df = pd.DataFrame(results)
results_df = results_df.sort_values("network_distance_km")

output_path = Path("data/processed")
output_path.mkdir(parents=True, exist_ok=True)

results_df.to_csv(
    output_path / "healthcare_accessibility.csv",
    index=False,
)

print("\n--- Nearest Healthcare Facilities ---")
print(results_df.head(10).to_string(index=False))

print("\nFacilities analysed:", len(results_df))
print(
    "Average network distance (km):",
    round(results_df["network_distance_km"].mean(), 2),
)
print("Results saved to data/processed/healthcare_accessibility.csv")

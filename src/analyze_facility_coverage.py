
import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Load existing datasets
G = ox.load_graphml("data/raw/delhi_walk_network.graphml")
grid = gpd.read_file("data/processed/analysis_grid.geojson")
services = gpd.read_file("data/raw/healthcare_services.geojson")

# Convert to latitude/longitude
grid = grid.to_crs("EPSG:4326")
services = services.to_crs("EPSG:4326")

# Convert facility polygons into representative points
# using a projected CRS for accurate geometry operations
services_projected = services.to_crs("EPSG:32643")
facility_points = services_projected.representative_point()
facility_points = gpd.GeoSeries(
    facility_points,
    crs="EPSG:32643"
).to_crs("EPSG:4326")

# Match locations to road-network nodes
grid_nodes = ox.distance.nearest_nodes(
    G, X=grid.geometry.x, Y=grid.geometry.y
)

service_nodes = ox.distance.nearest_nodes(
    G, X=facility_points.x, Y=facility_points.y
)

# Calculate facility coverage
results = []

for i, grid_node in enumerate(grid_nodes):

    distances = nx.single_source_dijkstra_path_length(
        G, grid_node, cutoff=1000, weight="length"
    )

    within_500m = sum(
        node in distances and distances[node] <= 500
        for node in service_nodes
    )

    within_1000m = sum(
        node in distances and distances[node] <= 1000
        for node in service_nodes
    )

    results.append({
        "grid_id": int(grid.iloc[i]["grid_id"]),
        "facilities_500m": within_500m,
        "facilities_1000m": within_1000m
    })

# Save results
output = Path("data/processed/facility_coverage.csv")
output.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(results)
df.to_csv(output, index=False)

print("Facility coverage analysis complete!")
print("Grid points analysed:", len(df))
print("Average facilities within 500m:", round(df["facilities_500m"].mean(), 2))
print("Average facilities within 1km:", round(df["facilities_1000m"].mean(), 2))
print("Grid points with zero facilities within 1km:",
      (df["facilities_1000m"] == 0).sum())
print("Saved to:", output)

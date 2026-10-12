
import osmnx as ox
import networkx as nx
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Load existing datasets
G = ox.load_graphml("data/raw/delhi_walk_network.graphml")
grid = gpd.read_file("data/processed/analysis_grid.geojson")
services = gpd.read_file("data/raw/healthcare_services.geojson")

# Keep only hospitals
hospitals = services[
    services["amenity"] == "hospital"
].copy()

print("Hospitals found:", len(hospitals))

# Convert to latitude/longitude
grid = grid.to_crs("EPSG:4326")
hospitals = hospitals.to_crs("EPSG:4326")

# Convert hospital polygons into representative points
hospitals_projected = hospitals.to_crs("EPSG:32643")

hospital_points = gpd.GeoSeries(
    hospitals_projected.representative_point(),
    crs="EPSG:32643"
).to_crs("EPSG:4326")

# Find nearest road-network nodes
grid_nodes = ox.distance.nearest_nodes(
    G,
    X=grid.geometry.x,
    Y=grid.geometry.y
)

hospital_nodes = ox.distance.nearest_nodes(
    G,
    X=hospital_points.x,
    Y=hospital_points.y
)

# Calculate hospital accessibility
results = []

for i, grid_node in enumerate(grid_nodes):

    distances = nx.single_source_dijkstra_path_length(
        G,
        source=grid_node,
        weight="length"
    )

    hospital_distances = [
        distances[node]
        for node in hospital_nodes
        if node in distances
    ]

    nearest_distance = (
        min(hospital_distances)
        if hospital_distances else None
    )

    within_500m = sum(
        distance <= 500
        for distance in hospital_distances
    )

    within_1000m = sum(
        distance <= 1000
        for distance in hospital_distances
    )

    results.append({
        "grid_id": int(grid.iloc[i]["grid_id"]),
        "nearest_hospital_km": (
            round(nearest_distance / 1000, 3)
            if nearest_distance is not None else None
        ),
        "hospitals_500m": within_500m,
        "hospitals_1000m": within_1000m
    })

# Save results
output = Path("data/processed/hospital_coverage.csv")
output.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(results)
df.to_csv(output, index=False)

print("\nHospital accessibility analysis complete!")
print("Grid points analysed:", len(df))
print(
    "Average nearest-hospital distance (km):",
    round(df["nearest_hospital_km"].mean(), 3)
)
print(
    "Average hospitals within 500m:",
    round(df["hospitals_500m"].mean(), 2)
)
print(
    "Average hospitals within 1km:",
    round(df["hospitals_1000m"].mean(), 2)
)
print(
    "Grid points with zero hospitals within 1km:",
    (df["hospitals_1000m"] == 0).sum()
)
print("Saved to:", output)

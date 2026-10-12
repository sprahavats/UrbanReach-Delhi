
import folium
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Load the grid and accessibility results
grid = gpd.read_file("data/processed/analysis_grid.geojson")
results = pd.read_csv("data/processed/grid_healthcare_accessibility.csv")

# Join accessibility results to grid locations
grid = grid.merge(results, on="grid_id")

# Create a map centred on the study area
centre_lat = grid.geometry.y.mean()
centre_lon = grid.geometry.x.mean()

m = folium.Map(
    location=[centre_lat, centre_lon],
    zoom_start=14,
    tiles="OpenStreetMap"
)

# Fixed distance categories (in km)
def classify_access(distance):
    if distance <= 0.5:
        return "Within 500 m"
    elif distance <= 1.0:
        return "500 m–1 km"
    elif distance <= 1.5:
        return "1–1.5 km"
    else:
        return "Over 1.5 km"

colours = {
    "Within 500 m": "green",
    "500 m–1 km": "yellow",
    "1–1.5 km": "orange",
    "Over 1.5 km": "red"
}

grid["access_category"] = grid["network_distance_km"].apply(
    classify_access
)

# Add grid points
for _, row in grid.iterrows():
    category = row["access_category"]
    distance = row["network_distance_km"]

    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=8,
        color=colours[category],
        fill=True,
        fill_color=colours[category],
        fill_opacity=0.85,
        tooltip=(
            f"Grid point: {row['grid_id']} | "
            f"Category: {category} | "
            f"Nearest facility: {row['nearest_service']} | "
            f"Network distance: {distance:.3f} km"
        )
    ).add_to(m)

# Add a clear legend
legend_html = """
<div style="
position: fixed;
bottom: 25px;
left: 25px;
z-index: 9999;
background: white;
padding: 12px;
border: 1px solid grey;
border-radius: 5px;
font-size: 13px;">
<b>Distance to nearest healthcare feature</b><br>
<span style="color:green;">●</span> Within 500 m<br>
<span style="color:#d4a900;">●</span> 500 m–1 km<br>
<span style="color:orange;">●</span> 1–1.5 km<br>
<span style="color:red;">●</span> Over 1.5 km
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# Save the interactive map
output_dir = Path("outputs/maps")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "grid_healthcare_accessibility.html"
m.save(output_path)

print("Grid accessibility map created!")
print("Grid points mapped:", len(grid))
print("\nGrid points by distance category:")
print(grid["access_category"].value_counts().to_string())
print("Saved to:", output_path)

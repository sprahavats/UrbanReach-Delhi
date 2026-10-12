
import folium
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Load data
services = gpd.read_file("data/raw/healthcare_services.geojson")
results = pd.read_csv("data/processed/healthcare_accessibility.csv")
reference = pd.read_csv("data/reference_points.csv")

latitude = float(reference.loc[0, "latitude"])
longitude = float(reference.loc[0, "longitude"])

# Create interactive map
m = folium.Map(
    location=[latitude, longitude],
    zoom_start=14,
    tiles="OpenStreetMap",
)

# Mark IIT Delhi reference point
folium.Marker(
    [latitude, longitude],
    popup="IIT Delhi reference point",
    tooltip="IIT Delhi",
    icon=folium.Icon(color="blue", icon="university", prefix="fa"),
).add_to(m)

# Add healthcare facilities
for _, service in services.iterrows():
    point = service.geometry.representative_point()
    name = service.get("name")
    amenity = service.get("amenity", "Unknown")

    folium.CircleMarker(
        location=[point.y, point.x],
        radius=5,
        color="red",
        fill=True,
        fill_opacity=0.75,
        popup=f"{name if pd.notna(name) else 'Unnamed facility'} — {amenity}",
    ).add_to(m)

# Save map
output_dir = Path("outputs/maps")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "healthcare_accessibility.html"
m.save(output_path)

print("Interactive map saved to:", output_path)

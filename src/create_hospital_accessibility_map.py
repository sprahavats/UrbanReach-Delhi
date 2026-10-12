
import folium
import geopandas as gpd
from pathlib import Path

# Load the classified grid dataset
grid = gpd.read_file("data/processed/underserved_areas.geojson")
grid = grid.to_crs("EPSG:4326")

# Create map centred on the study area
centre_lat = grid.geometry.y.mean()
centre_lon = grid.geometry.x.mean()

m = folium.Map(
    location=[centre_lat, centre_lon],
    zoom_start=14,
    tiles="OpenStreetMap"
)

# Colour categories by hospital accessibility
colours = {
    "No hospital within 1 km": "red",
    "One hospital within 1 km": "orange",
    "Multiple hospitals within 1 km": "green"
}

# Add each grid point
for _, row in grid.iterrows():
    category = row["hospital_access_category"]
    colour = colours[category]

    nearest_distance = row["nearest_hospital_km"]
    distance_text = (
        f"{nearest_distance:.3f} km"
        if nearest_distance is not None
        else "Not available"
    )

    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=8,
        color=colour,
        fill=True,
        fill_color=colour,
        fill_opacity=0.85,
        tooltip=(
            f"Grid point: {row['grid_id']} | "
            f"Category: {category} | "
            f"Nearest hospital: {distance_text}"
        )
    ).add_to(m)

# Add a legend
legend_html = """
<div style="
position: fixed;
bottom: 30px;
left: 30px;
z-index: 9999;
background: white;
padding: 12px;
border: 1px solid grey;
border-radius: 5px;
font-size: 13px;">
<b>Hospital accessibility</b><br>
<span style="color:red;">●</span> No hospital within 1 km<br>
<span style="color:orange;">●</span> One hospital within 1 km<br>
<span style="color:green;">●</span> Multiple hospitals within 1 km
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# Save map
output_dir = Path("outputs/maps")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "hospital_accessibility_map.html"
m.save(output_path)

print("Hospital accessibility map created!")
print("Grid points mapped:", len(grid))
print("Saved to:", output_path)


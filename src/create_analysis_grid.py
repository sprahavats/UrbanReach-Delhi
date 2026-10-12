
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path

# Approximate centre of IIT Delhi
latitude = 28.5450
longitude = 77.1926

# Create a local projected coordinate system in metres
centre = gpd.GeoDataFrame(
    geometry=[Point(longitude, latitude)],
    crs="EPSG:4326",
).to_crs("EPSG:32643")

x_centre = centre.geometry.iloc[0].x
y_centre = centre.geometry.iloc[0].y

# Generate grid points at 500-metre spacing
spacing = 500
radius = 2000
points = []


for x_offset in range(-radius, radius + 1, spacing):
    for y_offset in range(-radius, radius + 1, spacing):
        # Keep points within the 2 km study radius
        if x_offset**2 + y_offset**2 <= radius**2:
            x = x_centre + x_offset
            y = y_centre + y_offset
            points.append(Point(x, y))


grid = gpd.GeoDataFrame(
    {"grid_id": range(1, len(points) + 1)},
    geometry=points,
    crs="EPSG:32643",
).to_crs("EPSG:4326")

# Save the grid
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "analysis_grid.geojson"
grid.to_file(output_path, driver="GeoJSON")

print("Analysis grid created!")
print("Number of grid points:", len(grid))
print("Grid spacing:", spacing, "metres")
print("Saved to:", output_path)

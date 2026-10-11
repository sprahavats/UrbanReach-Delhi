
import osmnx as ox
from pathlib import Path

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

latitude = 28.5450
longitude = 77.1926

print("Downloading healthcare facilities...")

tags = {
    "amenity": ["hospital", "clinic", "doctors", "pharmacy"]
}

services = ox.features_from_point(
    (latitude, longitude),
    tags=tags,
    dist=2000,
)

print("Download successful!")
print("Healthcare features found:", len(services))

output_path = output_dir / "healthcare_services.geojson"
services = services.reset_index()
services.to_file(output_path, driver="GeoJSON")

print("Saved to:", output_path)


print("\n--- Healthcare Data Preview ---")

print(
    services[["name", "amenity", "geometry"]]
    .head(10)
    .to_string(index=False)
)

print("\nFeature counts by type:")
print(services["amenity"].value_counts(dropna=False))

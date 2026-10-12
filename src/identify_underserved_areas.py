
import geopandas as gpd
import pandas as pd
from pathlib import Path

# Load the grid and both coverage datasets
grid = gpd.read_file("data/processed/analysis_grid.geojson")
all_healthcare = pd.read_csv("data/processed/facility_coverage.csv")
hospital_data = pd.read_csv("data/processed/hospital_coverage.csv")

# Combine the results by grid ID
results = all_healthcare.merge(
    hospital_data,
    on="grid_id",
    how="inner"
)

# Add the grid locations
grid = grid.merge(results, on="grid_id", how="inner")

# Classify hospital accessibility
def classify_access(count):
    if count == 0:
        return "No hospital within 1 km"
    elif count == 1:
        return "One hospital within 1 km"
    else:
        return "Multiple hospitals within 1 km"

grid["hospital_access_category"] = (
    grid["hospitals_1000m"].apply(classify_access)
)

# Flag locations with no hospital within 1 km
grid["potentially_underserved"] = (
    grid["hospitals_1000m"] == 0
)

# Save the combined results
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

csv_path = output_dir / "underserved_areas.csv"
geojson_path = output_dir / "underserved_areas.geojson"

grid.drop(columns="geometry").to_csv(csv_path, index=False)
grid.to_file(geojson_path, driver="GeoJSON")

# Print summary statistics
print("Underserved-area analysis complete!")
print("Grid points classified:", len(grid))
print("\nHospital accessibility categories:")
print(grid["hospital_access_category"].value_counts().to_string())
print(
    "\nPotentially underserved grid points:",
    int(grid["potentially_underserved"].sum())
)
print("Saved CSV:", csv_path)
print("Saved spatial dataset:", geojson_path)


import pandas as pd
from pathlib import Path

# Input datasets
facility_path = Path("data/processed/facility_coverage.csv")
hospital_path = Path("data/processed/hospital_coverage.csv")

# Output dataset
output_path = Path("data/processed/healthcare_hospital_comparison.csv")

# Load datasets
facilities = pd.read_csv(facility_path)
hospitals = pd.read_csv(hospital_path)

# Combine results using grid point IDs
comparison = facilities.merge(
    hospitals,
    on="grid_id",
    validate="one_to_one"
)

print("GRID POINTS:", len(comparison))

print("\nAVERAGE COVERAGE")
print(
    "Healthcare features within 500 m:",
    round(comparison["facilities_500m"].mean(), 2)
)
print(
    "Healthcare features within 1 km:",
    round(comparison["facilities_1000m"].mean(), 2)
)
print(
    "Hospitals within 500 m:",
    round(comparison["hospitals_500m"].mean(), 2)
)
print(
    "Hospitals within 1 km:",
    round(comparison["hospitals_1000m"].mean(), 2)
)

print("\nDISTANCE")
print(
    "Average nearest-hospital distance (km):",
    round(comparison["nearest_hospital_km"].mean(), 3)
)

print(
    "\nGRID POINTS WITH ZERO FACILITIES WITHIN 1 KM:",
    int((comparison["facilities_1000m"] == 0).sum())
)
print(
    "GRID POINTS WITH ZERO HOSPITALS WITHIN 1 KM:",
    int((comparison["hospitals_1000m"] == 0).sum())
)

# Save the combined dataset
output_path.parent.mkdir(parents=True, exist_ok=True)
comparison.to_csv(output_path, index=False)

print("\nSaved:", output_path)


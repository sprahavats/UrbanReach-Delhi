# UrbanReach-Delhi: GIS-Based Urban Accessibility and Road-Network Analysis

## Overview

UrbanReach-Delhi is a geospatial research project investigating walking-network accessibility to healthcare services around IIT Delhi, South Delhi. The project combines OpenStreetMap data, graph-based shortest-path analysis, spatial grids, and interactive maps to examine how access to general healthcare features differs from access to hospitals.

The workflow uses Python-based geospatial tools and QGIS for spatial analysis and visualisation.

## Research Questions

1. How accessible are mapped healthcare services across locations within the study area?
2. How does accessibility to hospitals differ from accessibility to healthcare services overall?
3. Which sampled locations have no mapped hospital within a 1 km walking-network distance?
4. How could changes to the road network affect access to essential services?

## Study Area

- **Reference location:** IIT Delhi, South Delhi, India
- **Study radius:** 2 km from the reference point
- **Spatial sampling:** 49 grid points at approximately 500 m spacing
- **Network:** OpenStreetMap walking network downloaded using OSMnx

The walking network extends approximately 3 km from the reference point to reduce boundary effects during route analysis.

## Technologies

- Python
- OSMnx
- NetworkX
- GeoPandas
- Shapely
- Pandas and NumPy
- Folium
- QGIS
- OpenStreetMap

## Methodology

1. Download and construct a walking network from OpenStreetMap.
2. Retrieve mapped healthcare features, including hospitals, clinics, pharmacies, and doctors.
3. Generate a regular spatial grid within the study area.
4. Estimate walking-network distances between grid locations and mapped healthcare features.
5. Calculate healthcare-feature and hospital coverage within 500 m and 1 km thresholds.
6. Identify locations with no mapped hospital within 1 km of network distance.
7. Generate interactive maps and tabular outputs for spatial comparison.

Distances are estimated using the available road graph and snapped network locations. Results depend on OpenStreetMap completeness, network coverage, and the accuracy of feature locations.

## Preliminary Findings

The analysis covers 49 grid points and 61 mapped healthcare features.

- **61 healthcare features:** 26 pharmacies, 18 hospitals, 16 clinics, and 1 doctor.
- **General healthcare coverage:** An average of 2.92 mapped healthcare features within 1 km of a grid point.
- **Hospital coverage:** An average of 1.08 mapped hospital features within 1 km.
- **Locations without a mapped healthcare feature within 1 km:** 4 of 49 grid points.
- **Locations without a mapped hospital within 1 km:** 20 of 49 grid points.
- **Average nearest-hospital network distance:** Approximately 0.98 km.

These are preliminary, feature-based results rather than population-weighted measures of healthcare access. Mapped features are not necessarily equivalent to verified, unique institutions.

## Repository Structure

```text
UrbanReach-Delhi/
├── src/
│   ├── download_network.py
│   ├── download_services.py
│   ├── check_network.py
│   ├── analyze_healthcare_access.py
│   ├── create_network_map.py
│   ├── create_accessibility_map.py
│   ├── create_analysis_grid.py
│   ├── analyze_grid_accessibility.py
│   ├── create_grid_accessibility_map.py
│   ├── analyze_facility_coverage.py
│   ├── analyze_hospital_coverage.py
│   ├── compare_healthcare_hospitals.py
│   ├── identify_underserved_areas.py
│   └── create_hospital_accessibility_map.py
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   ├── maps/
│   └── figures/
├── reports/
│   └── UrbanReach_Research_Report.md
├── requirements.txt
└── README.md
```

Downloaded datasets and generated outputs are excluded from Git by `.gitignore`. Run the relevant scripts to regenerate them.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/sprahavats/UrbanReach-Delhi.git
cd UrbanReach-Delhi
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Generate the data and analyses

Run scripts from the repository root, with the virtual environment activated.

For a fresh setup, download the walking network and healthcare features first:

```bash
python src/download_network.py
python src/download_services.py
```

Then generate the grid and run the analyses:

```bash
python src/create_analysis_grid.py
python src/analyze_grid_accessibility.py
python src/analyze_facility_coverage.py
python src/analyze_hospital_coverage.py
python src/compare_healthcare_hospitals.py
python src/identify_underserved_areas.py
```

Generate the interactive maps:

```bash
python src/create_network_map.py
python src/create_accessibility_map.py
python src/create_grid_accessibility_map.py
python src/create_hospital_accessibility_map.py
```

Some scripts depend on outputs generated by earlier scripts. Run them in the order shown above. The network download and service retrieval require an internet connection.

## Outputs

The workflow generates:

- Walking-network data and network diagnostics
- Healthcare accessibility tables
- Grid-based accessibility estimates
- Healthcare-feature and hospital coverage statistics
- A comparison of general healthcare and hospital coverage
- A screening layer for locations with no mapped hospital within 1 km
- Interactive network and accessibility maps
- A detailed research report

## Limitations

- OpenStreetMap may omit facilities or contain outdated information.
- Mapped features may not correspond one-to-one with unique healthcare institutions.
- The grid is not weighted by population or demographic need.
- Distance thresholds do not measure travel time, facility capacity, affordability, or quality of care.
- Snapping facilities and grid points to road-network nodes introduces approximation error.
- Network disruption simulations and expanded essential-service categories remain future work.

Locations flagged as potentially underserved should be interpreted as candidates for further investigation, not proof of inadequate healthcare provision.

## Future Work

- Validate mapped facilities and improve duplicate handling.
- Expand the analysis to additional essential-service categories.
- Add population-weighted accessibility measures.
- Simulate road closures and network improvements.
- Produce publication-quality statistical figures and maps.
- Improve automated reproducibility and document validation checks.

## Research Report

See [`reports/UrbanReach_Research_Report.md`](reports/UrbanReach_Research_Report.md) for the full methodology, preliminary findings, discussion, limitations, and references.

## Data and Attribution

Road-network and healthcare-feature data are sourced from [OpenStreetMap](https://www.openstreetmap.org/). OpenStreetMap data are available under the Open Database License (ODbL). Please consult the relevant attribution and licensing requirements when redistributing data or derived datasets.

## Author

**Spraha Vats**  
IIT Delhi — B.Tech., Civil Engineering

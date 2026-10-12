
# UrbanReach-Delhi: GIS-Based Urban Accessibility and Road-Network Analysis

**Project type:** Geospatial analysis and urban accessibility  
**Study area:** A 2 km radius around IIT Delhi, New Delhi, India  
**Tools:** Python, OSMnx, NetworkX, GeoPandas, Pandas, Folium, QGIS  
**Status:** Preliminary analysis

---

## Abstract

Access to essential healthcare services depends not only on the number of facilities available but also on their spatial distribution and connectivity through the road network. This project develops a GIS-based workflow to examine walking-network accessibility to mapped healthcare facilities around IIT Delhi in New Delhi.

OpenStreetMap data are used to construct a pedestrian network and identify mapped healthcare features, including hospitals, clinics, pharmacies, and doctors. The study area is represented by 49 grid points arranged at approximately 500 m spacing within a 2 km radius of the study centre. Network-based distances and facility counts are calculated for each point, allowing general healthcare availability to be compared with hospital-specific accessibility.

Preliminary results indicate that the average number of mapped healthcare features within 1 km is 2.92 per grid point, while the average number of mapped hospitals within the same distance is 1.08. Twenty of the 49 grid points have no mapped hospital within 1 km of network distance. These results illustrate how accessibility estimates can differ depending on the type of healthcare facility considered.

The analysis is exploratory. Results depend on OpenStreetMap completeness, the selected study area, network construction, and the use of regularly spaced grid points rather than population-weighted locations.

---

## 1. Introduction

Urban accessibility is an important consideration in transport planning and the spatial distribution of essential services. Straight-line proximity alone may not represent practical access because pedestrians must travel through a connected network of roads and paths.

Geographic Information Systems (GIS), open geospatial data, and graph-based network analysis provide tools for examining these relationships. By representing the walking network as a graph, shortest-path algorithms can estimate the network distance between locations and nearby facilities.

Healthcare access is particularly important to investigate because different facility types serve different functions. A pharmacy or clinic may be relatively close to a location even when a hospital is not. Combining all healthcare features into one measure can therefore conceal differences in hospital accessibility.

This project develops a reproducible workflow for mapping and comparing general healthcare-feature coverage and hospital-specific walking-network accessibility around IIT Delhi.

### 1.1 Research question

How does walking-network accessibility to mapped healthcare facilities vary across a 2 km study area around IIT Delhi, and how does general healthcare-feature coverage differ from hospital accessibility?

### 1.2 Objectives

1. Construct and inspect a pedestrian road network using OpenStreetMap data.
2. Identify mapped healthcare features within the study area.
3. Generate a spatial grid for consistent accessibility comparisons.
4. Estimate network-based distances and count mapped facilities within selected distance thresholds.
5. Identify grid points with no mapped hospital within 1 km.
6. Produce interactive maps and reproducible datasets for further investigation.

---

## 2. Study Area and Data

### 2.1 Study area

The analysis is centred approximately on IIT Delhi at latitude 28.5450° N and longitude 77.1926° E. The intended analysis area extends 2 km from this centre.

A regular grid with approximately 500 m spacing is used to sample locations across the study area. After spatial filtering, 49 grid points are included in the analysis.

These grid points are analytical sample locations. They do not represent individual residents, households, or equally populated neighbourhoods.

### 2.2 Data sources

OpenStreetMap (OSM) provides the underlying road-network and healthcare-feature data.

The walking network is downloaded using OSMnx with the `walk` network type. Healthcare features are retrieved using OSM amenity tags covering hospitals, clinics, doctors, and pharmacies.

The downloaded healthcare dataset contains 61 mapped features:

| Feature type | Mapped features |
|---|---:|
| Pharmacies | 26 |
| Hospitals | 18 |
| Clinics | 16 |
| Doctors | 1 |
| **Total** | **61** |

Three features have no recorded name. No exact duplicate geometries were detected in the initial geometry check. However, different mapped features may still correspond to the same institution or facility, so these counts should not automatically be interpreted as counts of unique healthcare institutions.

### 2.3 Walking-network dataset

The final downloaded walking network contains:

- 6,718 nodes
- 18,306 edges
- One weakly connected component
- A strongly connected graph according to the network validation check

The network download radius was expanded to 3 km to provide additional routing coverage beyond the 2 km analysis area and reduce edge effects.

The graph's connectivity checks describe the downloaded graph, not the completeness or quality of every pedestrian route. Connectivity also does not establish that every mapped route is safe, accessible, or legally usable by all pedestrians.

---

## 3. Methodology

### 3.1 Network construction

OSMnx is used to download the walking network from OpenStreetMap. The network is represented as a graph in which nodes represent mapped junctions or locations and edges represent walkable network segments.

The graph is saved in GraphML format for reuse. Node and edge layers are exported to GeoJSON for inspection in QGIS.

### 3.2 Healthcare-feature mapping

Mapped healthcare features are downloaded using OSM amenity tags for hospitals, clinics, doctors, and pharmacies.

The general healthcare analysis includes all retrieved feature types. The hospital-specific analysis filters the dataset to features tagged as hospitals.

OpenStreetMap classifications and completeness may vary, and the dataset does not establish service capacity, quality, opening hours, or current operational status.

### 3.3 Grid generation

A circular study area with a 2 km radius is sampled using grid points spaced approximately 500 m apart. The resulting 49 locations provide a consistent set of points for comparing accessibility measures.

The grid is used as a spatial sampling framework rather than a population distribution model.

### 3.4 Network-distance estimation

Shortest-path calculations are performed on the walking network. Grid locations and healthcare features are associated with nearby network nodes so that distances can be calculated along the graph.

For each grid point, the analysis estimates the distance to the nearest mapped healthcare feature and the nearest mapped hospital. It also counts mapped features within 500 m and 1 km of network distance.

Network distances differ from straight-line distances because routes follow the available pedestrian network.

### 3.5 Accessibility classification

For the hospital analysis, grid points are grouped into three categories according to the number of mapped hospitals within 1 km:

- No hospital within 1 km
- One hospital within 1 km
- Multiple hospitals within 1 km

Grid points with no mapped hospital within 1 km are flagged as potentially underserved for further investigation. This is a screening indicator, not a definitive measure of unmet healthcare need.

For the general healthcare map, nearest-feature distances are classified into four exploratory bands:

- Within 500 m
- More than 500 m and up to 1 km
- More than 1 km and up to 1.5 km
- More than 1.5 km

These thresholds are used for visual interpretation and are not presented as official healthcare-access standards.

### 3.6 Software and reproducibility

The workflow uses Python, OSMnx, NetworkX, GeoPandas, Pandas, and Folium. QGIS is used to inspect spatial layers and maps.

Scripts and dependencies are maintained in the project repository. Downloaded data and generated outputs are stored separately from source code.

---

## 4. Results

### 4.1 General healthcare-feature coverage

Across the 49 grid points:

| Metric | Result |
|---|---:|
| Average mapped features within 500 m | 0.84 |
| Average mapped features within 1 km | 2.92 |
| Grid points with zero mapped features within 1 km | 4 of 49 |
| Average nearest-feature network distance | 0.571 km |

The nearest-feature distance distribution is:

| Statistic | Distance |
|---|---:|
| Minimum | 0.039 km |
| 25th percentile | 0.267 km |
| Median | 0.493 km |
| 75th percentile | 0.788 km |
| Maximum | 2.212 km |
| Mean | 0.571 km |

Twenty-five grid points have a nearest mapped healthcare feature within 500 m. Twenty points have a nearest feature more than 500 m and up to 1 km away. Three points fall in the 1–1.5 km band, and one point is beyond 1.5 km.

These values describe the mapped healthcare features and the sampled grid points, not the percentage of residents with access to healthcare.

### 4.2 Hospital accessibility

The hospital-specific analysis identifies 18 mapped features tagged as hospitals.

| Metric | Result |
|---|---:|
| Average nearest-hospital network distance | 0.98 km |
| Average mapped hospitals within 500 m | 0.27 |
| Average mapped hospitals within 1 km | 1.08 |
| Grid points with no mapped hospital within 1 km | 20 of 49 |

The 49 grid points are classified as follows:

| Hospital-access category | Grid points |
|---|---:|
| No hospital within 1 km | 20 |
| One hospital within 1 km | 17 |
| Multiple hospitals within 1 km | 12 |
| **Total** | **49** |

Approximately 40.8% of the sampled grid points have no mapped hospital within 1 km of network distance.

This result identifies locations for further examination. It does not prove that the surrounding population lacks adequate hospital access, since the analysis does not account for population, hospital capacity, alternative transport modes, or healthcare-seeking behaviour.

### 4.3 Comparison between general healthcare and hospitals

| Metric | All mapped healthcare features | Hospitals only |
|---|---:|---:|
| Average features within 500 m | 0.84 | 0.27 |
| Average features within 1 km | 2.92 | 1.08 |
| Grid points with zero features within 1 km | 4 (8.2%) | 20 (40.8%) |

The comparison shows that general healthcare-feature coverage is more widespread than hospital coverage in the study area.

The distinction matters because pharmacies, clinics, doctors, and hospitals provide different services. A location close to a pharmacy or clinic may still be relatively far from a hospital.

### 4.4 Spatial outputs

The project generates the following principal outputs:

- Walking-network node and edge layers for QGIS
- Interactive general healthcare accessibility map
- Interactive hospital accessibility map
- Grid-based healthcare accessibility dataset
- General facility coverage dataset
- Hospital coverage dataset
- Potentially underserved-area dataset
- Combined healthcare-versus-hospital comparison CSV

The interactive maps allow individual grid points to be inspected, including their categories and calculated distances.

---

## 5. Discussion

The preliminary results demonstrate the value of distinguishing general healthcare-feature availability from hospital-specific accessibility. Across the sampled grid points, the average number of mapped healthcare features within 1 km is 2.92, compared with 1.08 mapped hospitals.

The difference between the two measures is also evident in the number of locations with no mapped feature within 1 km. Four grid points have no mapped healthcare feature within this threshold, while 20 have no mapped hospital within it.

These results suggest that conclusions about healthcare accessibility depend on the service category being investigated. A single measure that combines all healthcare features may obscure gaps in access to particular types of care.

Network-based distances provide a more realistic representation of pedestrian travel than straight-line distances when the network is adequately mapped. However, the estimates remain sensitive to the network's coverage, the method used to associate locations with network nodes, and the accuracy of mapped facility locations.

The current work is best interpreted as a preliminary spatial screening analysis. It establishes a reproducible foundation for more detailed urban-accessibility research.

---

## 6. Limitations

1. **OpenStreetMap completeness:** Some roads, pedestrian paths, or healthcare features may be missing or incorrectly classified.
2. **Facility identity:** Different mapped features may represent the same institution, so counts do not necessarily represent unique facilities.
3. **Network representation:** Locations are associated with nearby network nodes. This approximation can affect calculated distances.
4. **Network boundaries:** Expanding the downloaded network to 3 km reduces, but does not eliminate, edge effects. Routes near the outer boundary may still be affected by missing network segments beyond it.
5. **Spatial sampling:** The 49 grid points are not population-weighted. Results cannot be interpreted as percentages of residents affected.
6. **Healthcare capacity:** The analysis does not consider bed availability, staffing, specialties, affordability, quality, opening hours, or service demand.
7. **Transport assumptions:** Walking distances do not capture travel by vehicle, public transport, or emergency ambulance.
8. **Exploratory thresholds:** The 500 m and 1 km thresholds are analytical choices, not official standards of adequate healthcare access.
9. **Geographic scope:** The study covers a limited area around IIT Delhi and should not be generalised to all of Delhi.

---

## 7. Future Work

Potential extensions include:

1. Validate facility locations and identify possible duplicate institutions.
2. Check route completeness and network-boundary sensitivity.
3. Add population data to estimate population-weighted accessibility.
4. Compare walking accessibility with other transport modes.
5. Investigate how road closures or network changes affect access to essential services.
6. Produce publication-quality maps and statistical figures.
7. Expand the analysis to additional essential-service categories.
8. Document the full setup and execution workflow in the project README.

---

## 8. Conclusion

This project develops a GIS-based workflow for analysing walking-network accessibility to mapped healthcare features around IIT Delhi. It combines OpenStreetMap data, graph-based shortest-path analysis, a regular spatial grid, and interactive visualisation.

The preliminary findings indicate that general healthcare-feature coverage is more widespread than hospital coverage across the 49 sampled grid points. Twenty locations have no mapped hospital within 1 km of network distance, compared with four locations with no mapped healthcare feature within the same threshold.

These results demonstrate why healthcare accessibility should be examined by service category rather than through a single combined facility count. Further work on data validation, population distribution, route completeness, and facility capacity is needed before making stronger claims about healthcare provision or unmet need.

---

## References

- OpenStreetMap contributors. OpenStreetMap geographic data. https://www.openstreetmap.org/
- Boeing, G. OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. *Computers, Environment and Urban Systems*, 65, 126–139, 2017.
- NetworkX documentation. https://networkx.org/documentation/stable/
- GeoPandas documentation. https://geopandas.org/
- Folium documentation. https://python-visualization.github.io/folium/


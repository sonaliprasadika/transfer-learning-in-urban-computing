import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Define the location
place_name = "Oulu, Finland"

# Define the PoI categories using OSM tags
tags = {
    "amenity": ["kindergarten", "school", "college", "university",  # Education
                "hospital", "clinic", "pharmacy",                   # Healthcare
                "restaurant", "cafe", "fast_food",                   # Food & Drinks
                "childcare", "nursery"]                              # Daycare
}

# Fetch PoI data
pois = ox.features_from_place(place_name, tags)

# Filter only Point geometries
pois_points = pois[pois.geometry.type == 'Point']

# Extract latitude & longitude from Point geometries
pois_points["latitude"] = pois_points.geometry.y  # Latitude from y
pois_points["longitude"] = pois_points.geometry.x  # Longitude from x

# Keep relevant columns and drop rows with missing names
pois_filtered = pois_points[["amenity", "name", "latitude", "longitude"]].dropna(subset=["name"])

# Save the corrected data to CSV
# pois_filtered.to_csv("poi_data_oulu_corrected.csv", index=False)

# Display first few results
print(pois_filtered[["name", "amenity", "latitude", "longitude"]].head())

# Create a GeoDataFrame for plotting
gdf = gpd.GeoDataFrame(pois_filtered, geometry=pois_points.geometry)

# Plot the map with points
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the base map of the region (OpenStreetMap data)
ox.plot_graph(ox.graph_from_place(place_name, network_type='all'), ax=ax, show=False, close=False)

# Plot the points (PoIs) on the map
gdf.plot(ax=ax, marker="o", color="red", markersize=50, label="PoIs")

# Add labels (names) for each point
for idx, row in gdf.iterrows():
    ax.text(
        row["longitude"] + 0.001, row["latitude"] + 0.001,  # Offset for label placement
        row["name"],
        fontsize=8, color="black", ha="left", va="bottom"
    )

# Set map title and labels
ax.set_title(f"PoIs in {place_name}", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.legend()
plt.show()
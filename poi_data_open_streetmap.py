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

# # Define the location (you can change this to any city or region)
# place_name = "Oulu, Finland"

# # 1. Get the street network
# G = ox.graph_from_place(place_name, network_type="drive")

# # Plot the street network
# ox.plot_graph(G)

# # Convert graph to GeoDataFrames
# nodes, edges = ox.graph_to_gdfs(G)

# # Plot the street network
# fig, ax = plt.subplots(figsize=(10, 10))
# ox.plot_graph(G, ax=ax, node_size=10, edge_linewidth=1, bgcolor="white")
# plt.title(f"Street Network of {place_name}")
# plt.show()

# # 2. Get building footprints
# buildings = ox.geometries_from_place(place_name, tags={"building": True})

# # Plot buildings
# fig, ax = plt.subplots(figsize=(10, 10))
# buildings.plot(ax=ax, color="gray", alpha=0.7)
# plt.title(f"Building Footprints of {place_name}")
# plt.show()

# # 3. Get points of interest (e.g., restaurants)
# pois = ox.geometries_from_place(place_name, tags={"amenity": "restaurant"})

# # Plot POIs
# fig, ax = plt.subplots(figsize=(10, 10))
# pois.plot(ax=ax, color="red", alpha=0.7)
# plt.title(f"Restaurants in {place_name}")
# plt.show()

# # 4. Get parks
# parks = ox.geometries_from_place(place_name, tags={"leisure": "park"})

# # Plot parks
# fig, ax = plt.subplots(figsize=(10, 10))
# parks.plot(ax=ax, color="green", alpha=0.5)
# plt.title(f"Parks in {place_name}")
# plt.show()

# # 5. Save Data to Files (optional)
# edges.to_file("streets.geojson", driver="GeoJSON")
# buildings.to_file("buildings.geojson", driver="GeoJSON")
# pois.to_file("restaurants.geojson", driver="GeoJSON")
# parks.to_file("parks.geojson", driver="GeoJSON")

# print("Data saved successfully!")


import json
import geopandas as gpd
from shapely.geometry import Point
import osmnx as ox

# Load JSON data from file
with open("tms_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract features from JSON
features = data.get("features", [])

# Convert to a list of dictionaries with geometry
pois_list = []
for feature in features:
    properties = feature["properties"]
    coordinates = feature["geometry"]["coordinates"]  # [longitude, latitude, altitude]
    longitude, latitude = coordinates[:2]  # Extract only lon, lat
    
    pois_list.append({
        "id": properties.get("id"),
        "name": properties.get("name", "Unknown"),
        "longitude": longitude,
        "latitude": latitude,
        "geometry": Point(longitude, latitude)
    })

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(pois_list, geometry="geometry", crs="EPSG:4326")

# Get Oulu boundary polygon from OpenStreetMap
oulu_boundary = ox.geocode_to_gdf("Oulu, Finland")

# Filter points that are inside the Oulu boundary
gdf_oulu = gdf[gdf.within(oulu_boundary.geometry.iloc[0])]

# Save filtered data
gdf_oulu.to_file("oulu_filtered_pois.geojson", driver="GeoJSON")

# Print filtered results
print(gdf_oulu)

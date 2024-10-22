import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

shapefile_path = (
    "IPCC-WGI-reference-regions-v4_shapefile/IPCC-WGI-reference-regions-v4.shp"
)
gdf = gpd.read_file(shapefile_path)

bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]

projections_dict = {
    "EPSG3857": "EPSG3857",
    "EPSG3395": "EPSG3395",
    "EPSG4326": "EPSG4326",
    "Simple": "Simple",
}

st.title("Map Projection Viewer")

projection_type = st.selectbox("Select a projection:", list(projections_dict.keys()))


m = leafmap.Map(
    locate_control=True,
    latlon_control=True,
    draw_export=True,
    minimap_control=True,
    crs=projections_dict[projection_type],
    center=center,
    zoom_start=6,
)

m.add_gdf(gdf, layer_name="IPCC Regions")


m.to_streamlit(height=700)

from pathlib import Path
import calendar
import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import xarray as xr
import streamlit as st
import pandas as pd

PROJECT_ROOT = Path.cwd()
DATA_PATH = PROJECT_ROOT / "data"


def plot_variable(data, date, projection="Robinson"):
    MEMBER = 1
    lon_, lat_ = data["lon"].values, data["lat"].values
    variable = data["t"].isel(member=MEMBER).sel(time=date)

    fig, ax = plt.subplots(figsize=(16, 12))
    if projection == "Robinson":
        m = Basemap(
            projection="robin",
            lon_0=0,
            resolution="c",
            llcrnrlat=-90,
            urcrnrlat=90,
            llcrnrlon=-180,
            urcrnrlon=180,
        )
    elif projection == "Stereographic":
        m = Basemap(projection="spstere", boundinglat=0, lon_0=270, resolution="l")

    # Draw coastlines and countries
    m.drawcoastlines()
    m.drawcountries()

    m.readshapefile(
        "data/IPCC-WGI-reference-regions-v4_shapefile/IPCC-WGI-reference-regions-v4",
        "Regions",
        drawbounds=True,
        color="white",
    )

    lon, lat = np.meshgrid(lon_, lat_)
    xi, yi = m(lon, lat)

    cs = m.pcolormesh(xi, yi, variable, cmap="jet")

    cbar = m.colorbar(cs, location="bottom", pad="10%")
    cbar.set_label("Data Units")

    st.pyplot(fig)


@st.cache_data
def load_data(file_path):
    return xr.open_dataset(file_path)


st.title("Climate Data Visualization")

filepath = DATA_PATH / "t_CMIP6_ssp370_mon_201501-210012.nc"
data = load_data(filepath)

years = range(2015, 2101)
months = range(1, 13)
month_names = [calendar.month_name[month] for month in months]
projections = ["Robinson", "Stereographic"]
dataset = ["CMIP6", "CMIP5"]
scenarios = ["SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5"]
variables = ["Temperature", "Precipitation"]


selected_projection = st.sidebar.selectbox("Select a projection", projections)
selected_dataset = st.sidebar.selectbox("Select a dataset", dataset)
selected_scenario = st.sidebar.selectbox("Select a scenario", scenarios)
selected_year = st.sidebar.selectbox("Select a year", years)
selected_month_name = st.sidebar.selectbox("Select a month", month_names)

selected_month = list(calendar.month_name).index(selected_month_name)
selected_date = datetime.datetime(selected_year, selected_month, 1)

# Plot the variable for the selected date
if st.sidebar.button("Plot Data"):
    plot_variable(data, selected_date, selected_projection)

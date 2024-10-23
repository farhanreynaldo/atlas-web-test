from pathlib import Path

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime
import numpy as np
import xarray as xr
import streamlit as st
import pandas as pd

PROJECT_ROOT = Path.cwd()
DATA_PATH = PROJECT_ROOT / "data"

def plot_variable(data, date):
    MEMBER = 1
    lon, lat = data['lon'].values, data['lat'].values
    variable = data['t'].isel(member=MEMBER).sel(time=date)

    fig,ax = plt.subplots(figsize=(16, 12))
    m = Basemap(projection='robin', lon_0=0, resolution='c', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)

    # Draw coastlines and countries
    m.drawcoastlines()
    m.drawcountries()

    lon, lat = np.meshgrid(lon, lat)
    xi, yi = m(lon, lat)

    cs = m.pcolormesh(xi, yi, variable, cmap='jet')

    cbar = m.colorbar(cs, location='right', pad='10%')
    cbar.set_label('Data Units')

    st.pyplot(fig)

@st.cache_data
def load_data(file_path):
    return xr.open_dataset(file_path)

st.title("Climate Data Visualization")

filepath =  DATA_PATH / "t_CMIP6_ssp370_mon_201501-210012.nc"
data = load_data(filepath)

dates = data['time'].values
years = sorted(list(set(pd.to_datetime(date).year for date in dates)))
months = sorted(list(set(pd.to_datetime(date).month for date in dates)))

selected_year = st.selectbox("Select a year", years)
selected_month = st.selectbox("Select a month", months)

selected_date = datetime.datetime(selected_year, selected_month, 1)

# Plot the variable for the selected date
if st.button("Plot Data"):
    plot_variable(data, selected_date)
    
    

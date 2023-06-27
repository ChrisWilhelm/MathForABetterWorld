"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from routeConnectors import locationConnectors
import json
from PIL import Image
import os

path = os.path.dirname(__file__)
image = Image.open(path + '/../assets/bmore_food_logo_dark_theme.png')
st.image(image)

st.title('Distrubution Maps')

df = pd.DataFrame(json.loads(locationConnectors.getVisitsPerLocation())["countByLocation"])
df = df.iloc[1:]

df['lat'] = df.apply(lambda x: x.location["latitude"], axis=1)
df['lat'] = pd.to_numeric(df['lat'], errors='coerce').astype(float)
df['lon'] = df.apply(lambda x: x.location["longitude"], axis=1)
df['lon'] = pd.to_numeric(df['lon'], errors='coerce').astype(float)
df['name'] = df.apply(lambda x: x.location["name"], axis=1)
count_map = px.scatter_mapbox(df, lat="lat", lon="lon", zoom=12, color = 'count', size = "count", color_continuous_scale='Jet', hover_data = {"name": True, "count": True, "lat":False, "lon": False})
# Update the mapbox style
count_map.update_layout(mapbox_style="open-street-map")
st.subheader("Map by Number of Deliverys")
st.plotly_chart(count_map)


df2 = pd.DataFrame(json.loads(locationConnectors.getWeightsPerLocation())["countByLocation"])
df2 = df2.iloc[1:]

df2['lat'] = df2.apply(lambda x: x.location["latitude"], axis=1)
df2['lat'] = pd.to_numeric(df['lat'], errors='coerce').astype(float)
df2['lon'] = df2.apply(lambda x: x.location["longitude"], axis=1)
df2['lon'] = pd.to_numeric(df['lon'], errors='coerce').astype(float)
df2['name'] = df2.apply(lambda x: x.location["name"], axis=1)
weight_map = px.scatter_mapbox(df2, lat="lat", lon="lon", zoom=12, color = 'sum', size = 'sum', color_continuous_scale='Jet', hover_data = {"name": True, "sum": True, "lat":False, "lon": False})
# Update the mapbox style
weight_map.update_layout(mapbox_style="open-street-map")
# Show the plot
st.subheader("Map by Weight of Export")
st.plotly_chart(weight_map)



#plot_dict = {'Count': count_map, "Weight": weight_map}
#plot_choice = st.selectbox('Choose a map', list(plot_dict.keys()))

#st.plotly_chart(plot_dict[plot_choice])
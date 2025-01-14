import streamlit as st
import datetime
import json
import urllib3
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape
from routeConnectors import locationConnectors
import os
from nav import nav_page
import pandas as pd

def getCoordinates(address):
    http = urllib3.PoolManager()
    str(address)
    r = http.request("GET", 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=AIzaSyBdwGpzITeG8YKCNozLvn4cKqQ7L-n8G2s', headers={'Content-Type': 'application/json'})
    jsonObj = json.loads(r.data.decode('utf-8'))
    if "error_message" in jsonObj:
        st.error("Please enter valid address")
        return "err", "err"
    else:
        lat = (jsonObj['results'][0]['geometry']['location']['lat'])
        lon = (jsonObj['results'][0]['geometry']['location']['lng'])
        return lat, lon

path = os.path.dirname(__file__)

st.set_page_config(layout="centered", page_icon=path + "/assets/bmore_food_logo_dark_theme.png", page_title="Location")
image = Image.open(path + '/../assets/bmore_food_logo_dark_theme.png')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image(image)
with col3:
    st.write(' ')

# log in status

if 'token' in st.session_state :
    log_button = st.button("Employee Log-out", key=".my-button", use_container_width=True)
else:
    log_button = st.button("Employee Log-in", key=".my-button", use_container_width=True)

print("getting locations...")
locations = locationConnectors.getLocations()["location"]
locationDF = pd.DataFrame(locations)

title_container = st.container()
col1, col2 = st.columns([1, 50])
with title_container:
    with col2:
        st.markdown("<h1 style='text-align: center; '>Locations Page</h1>", unsafe_allow_html=True)

if 'token' in st.session_state:
    editType = st.selectbox("Modification Type (Add, Edit) (Select Below)", ["", "New Location", "Update Location"])
    if editType == "New Location":
        with st.form("template_form"):
            name = st.text_input("Location Name", "")
            address = st.text_input(label = "Address of Location")
            newSubmit = st.form_submit_button()
            if newSubmit:
                if name == "":
                    st.error("Please fill in form elements!")
                else:
                    latitude, longitude = getCoordinates(address)
                    if latitude != "err":
                        newLoc = locationConnectors.postLocation(name, str(longitude), str(latitude))
                        st.experimental_rerun()
    elif editType == "Update Location":
        with st.form("template_form"):
            left, right = st.columns(2)
            idx = left.number_input("Id", min_value=1)
            name = st.text_input("Location Name", "")
            address = st.text_input(label = "Address of Location")
            editSubmit = st.form_submit_button()
            if editSubmit:
                if name == "":
                    st.error("Please fill in both form elements!")
                elif idx in locationDF.id.unique():
                    latitude, longitude = getCoordinates(address)
                    if latitude != "err":
                        editedLoc = locationConnectors.updateLocation(idx, name, str(longitude), str(latitude))
                        st.experimental_rerun()
                else:
                    st.error("Please input an id that is in the table!")

st.dataframe(locationDF)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

if log_button :
    if "token" in st.session_state :
        if "role" in st.session_state :
            del st.session_state.role
        del st.session_state.token
        st.experimental_rerun()
    else:
        nav_page("")
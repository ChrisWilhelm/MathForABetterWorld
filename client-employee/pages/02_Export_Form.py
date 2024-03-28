# import pdfkit
import streamlit as st
from PIL import Image
import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os 
from routeConnectors import categoryConnectors, locationConnectors, userConnector, exportConnectors
import json
import pandas as pd
from nav import nav_page

path = os.path.dirname(__file__)

st.set_page_config(layout="centered", page_icon=path + "/assets/bmore_food_logo_dark_theme.png", page_title="Export Form")
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


title_container = st.container()
col1, col2 = st.columns([1, 50])
with title_container:
    # with col1:
    #     st.image(path + '/../assets/bmore_food_logo_dark_theme.png', width=60)
    with col2:
        st.markdown("<h1 style='text-align: center; '>Food export form</h1>", unsafe_allow_html=True)
users = userConnector.getUsers()

locations = [{"id": -1, "name": "", "longitude":"", "latitude": ""}]  + locationConnectors.getLocations()['location']
allLocations = sorted(locations, key=lambda location: location["name"])

categories = [{"id": -1, "name": "", "description": ""}]  + categoryConnectors.getCategories()['category']
allCategories = sorted(categories, key=lambda cat: cat["name"])
users = [{"id": -1, "name": "", "email": ""}] + json.loads(userConnector.getUsers())['users']
allUsers = sorted(users, key=lambda use: use["name"])

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())


with st.form("template_form"):
    left, right = st.columns(2)
    location = left.selectbox("Location (Who Food Was Donated To)", allLocations, format_func=lambda loc: f'{loc["name"]}')
    category = right.selectbox("Category", allCategories, format_func=lambda cat: f'{cat["name"]}')
    exportType = left.selectbox("Export Type", (["Regular", "Damaged", "Recycle", "Compost", "Return"]))
    weight = right.text_input("Weight", value="")
    exportedBy = left.selectbox("User", allUsers, format_func=lambda use: f'{use["name"]}')
    submit = st.form_submit_button()

### TODO:: update userID when sign in functionality is implemented
if submit:
    categoryIndex = category["id"]
    locationIndex = location["id"]
    if weight == "" or locationIndex == -1 or categoryIndex == -1 or exportType == "" or exportedBy['id'] == -1:
        st.error('Please fill out the form')
    else:
        r = json.loads(exportConnectors.postExport(exportedBy["id"], categoryIndex, int(weight), location["id"], exportType))
        if "msg" not in r:
            st.balloons()
            st.success("🎉 Your export was generated!")
        else:
            st.error(r["msg"])

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

if log_button :
    if "token" in st.session_state :
        del st.session_state.token
        st.experimental_rerun()
    else:
        nav_page("")
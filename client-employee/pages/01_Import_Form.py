# import pdfkit
import streamlit as st
import datetime
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape
from routeConnectors import pallet
from routeConnectors import distributorConnectors
from routeConnectors import rackConnector
from routeConnectors import categoryConnectors
from routeConnectors import shiftConnector
import json
import os
from nav import nav_page
import pandas as pd

path = os.path.dirname(__file__)

st.set_page_config(layout="centered", page_icon=path + "/assets/bmore_food_logo_dark_theme.png", page_title="Import Form")
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

# Get rack, distributor and category info 
allRacks = [{"id": -1, "location": "", "description": "", "weightLimit": 0}]
rackRes = rackConnector.getRacks()
if rackRes: 
    allRacks = allRacks + rackRes["rack"]

distributors = [{"id": -1, "name": "", "description": ""}]  + distributorConnectors.getDistributors()['distributors']
allDistributors = sorted(distributors, key=lambda cat: cat["name"])

categories = [{"id": -1, "name": "", "description": ""}]  + categoryConnectors.getCategories()['category']
allCategories = sorted(categories, key=lambda cat: cat["name"])


allUsers = [{"id": -1, "name": ""}]
active_shifts = shiftConnector.activeShifts()
active_shifts2 = json.loads(active_shifts)
shifts = pd.json_normalize(active_shifts2["activeShifts"])
if shifts.empty:
    allUsers = []
else:
    allUsers = allUsers + shifts.apply(lambda x: {'id': x['user.id'], 'name': x['user.name']}, axis=1).tolist()

title_container = st.container()
col1, col2 = st.columns([1, 50])
with title_container:
    # with col1:
    #     st.image(image, width=200)
    with col2:
        st.markdown("<h1 style='text-align: center; '>Food import form</h1>", unsafe_allow_html=True)


env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
# template = env.get_template("invoice_template.html")

todaysDate = datetime.date.today()
with st.form("template_form"):
    left, right = st.columns(2)
    expiration_date = left.date_input("Expiration Date (Optional; Leave as 1970 if No Exp. Date)", value=datetime.date(1970, 1, 1))
    category = right.selectbox("Category", allCategories, format_func=lambda cat: f'{cat["name"]}')
    rack = left.selectbox("Rack (Optional)", allRacks, format_func=lambda rack: f'{rack["location"]}') # get more info on how racks are stored in the google form 
    distributor= right.selectbox("Distributor Name", allDistributors, format_func=lambda dis: f'{dis["name"]}')
    pallet_weight = left.text_input("Weight", value="1000")
    inputUser = right.selectbox("User", allUsers, format_func=lambda user: f'{user["name"]}' )
    description = st.text_input("Description (Optional)", value="")
    submit = st.form_submit_button()

if submit:
    if pallet_weight == "" or category['id'] == -1 or distributor["id"] == -1 or inputUser['id'] == -1:
        st.error('Please fill out the form')
    else:
        r = json.loads(pallet.postFood(
            inputUser["id"],
            todaysDate, 
            expiration_date, 
            pallet_weight, 
            distributor['id'],
            rack["id"],
            (description if description != "" else category["description"]),
            category['id']
        ))
        if "msg" not in r:
            st.balloons()
            st.success("🎉 Your import was generated!")
        else:
            st.error(r["msg"])

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
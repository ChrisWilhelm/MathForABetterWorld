# import pdfkit
import streamlit as st
import datetime
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape
from routeConnectors import foodEntry
import os

path = os.path.dirname(__file__)

st.set_page_config(layout="centered", page_icon="🍏", page_title="Bmore Food")
st.title("🍏 Bmore Food")

st.write(
    "Food import form!"
)

image = Image.open(path + '/../assets/bmore_food_logo.png')
col1, col2, col3 = st.columns(3)

with col1:
    st.image(image)
with col2:
    st.markdown("<h1>Food import form</h1>", unsafe_allow_html=True)



env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
# template = env.get_template("invoice_template.html")

todaysDate = datetime.date.today()
with st.form("template_form"):
    left, right = st.columns(2)
    expiration_date = left.date_input("Expiration date", value=datetime.date(2023, 1, 1))
    distributor_name = left.selectbox("Distributor name", ["Dole", "Amazon", ""])
    rack = right.text_input("Rack", value="12") # get more info on how racks are stored in the google form 
    pallet_weight = left.text_input("Weight", value="1000")
    category = right.selectbox("Category", ["Dairy", "Produce"])
    description = st.text_input("Description", value="")
    submit = st.form_submit_button()

if submit:
    st.balloons()
    st.write(expiration_date)

    ### TODO:: update userID when sign in functionality is implemented
    foodEntry.postFood(
        "userID",
        todaysDate, 
        expiration_date, 
        pallet_weight, 
        distributor_name,
        rack,
        True,
        description,
        category)

    
    st.success("🎉 Your import was generated!")

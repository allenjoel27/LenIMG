import requests
import streamlit as st
import base64
import io
from PIL import Image
import time

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Use raw string to avoid unicode escape error
desktop_img = get_img_as_base64(r"LenIMG bg.png")
mobile_img = get_img_as_base64(r"LenIMG bg_mobile.png")

page_bg_img = f"""
<style>
/* Default background for desktop */
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{desktop_img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}

/* Background for mobile devices */
@media only screen and (max-width: 768px) {{
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{mobile_img}");
        background-size: cover;
        background-position: center;
        background-attachment: scroll;
        background-repeat: no-repeat;
    }}
}}

[data-testid="stAppViewContainer"] {{
    overflow: hidden;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

/* Style the text input for visibility */
input[type="text"] {{
    color: black !important;
    background-color: rgba(255, 255, 255, 0.8) !important;
    border: 1px solid #ccc !important;
    border-radius: 4px !important;
    padding: 8px !important;
    font-size: 16px !important;
}}

::placeholder {{
    color: #666 !important;
    opacity: 1 !important;
}}

/* Center the Generate button and set the color to blue */
div.stButton > button {{
    display: inline-block;
    background-color: #5271ff; /* Blue background */
    color: white; /* White text */
    border: none; /* Remove borders */
    padding: 10px 24px; /* Some padding */
    text-align: center; /* Centered text */
    text-decoration: none; /* Remove underline */
    font-size: 16px; /* Increase font size */
    cursor: pointer; /* Pointer/hand icon */
    border-radius: 4px; /* Rounded corners */
}}

div.stButton > button:hover {{
    background-color: #4056d9; /* Darker blue on hover */
}}

/* Style for loader text */
#loader-text {{
    display: inline-block;
    margin-left: 10px;
    font-size: 16px;
    color: #666;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

prompt = st.text_input("Hey, Welcome to LenIMG! Input your prompt to generate an image")

if st.button("Generate"):
    with st.spinner('Your image is generating...'):
        time.sleep(2)  # Simulating a delay for the loader to appear
        image_bytes = query({"inputs": prompt})
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image)

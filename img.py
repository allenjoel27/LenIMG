import requests
import streamlit as st
import base64
import io
from PIL import Image

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Use raw string to avoid unicode escape error
img = get_img_as_base64(r"https://github.com/allenjoel27/LenIMG/blob/main/LenIMG%20bg.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
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
    image_bytes = query({"inputs": prompt})
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image)

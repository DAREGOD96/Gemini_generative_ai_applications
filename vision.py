from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import pathlib
import os
import textwrap
import google.generativeai as genai
from PIL import Image
from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


api = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api)


def get_response_from_gemini_vision(query, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if query != "":
        response = model.generate_content([query, image])
    else:
        response = model.generate_content(image)

    return response.text


st.set_page_config(page_title="Q&A using Gemini-vision model")
st.header("Gemini-vision-demo application")
input = st.text_input("enter your text here:", key="input")
user_uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if user_uploaded_file is not None:
    image = Image.open(user_uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Submit")

if submit:
    response = get_response_from_gemini_vision(query=input, image=image)
    st.subheader("The Response is")
    st.write(response)

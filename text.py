from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(questions):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(questions)
    return response.text


st.set_page_config(page_title="Q&A app using gemini-pro model")
st.header("Gemini Application")
input = st.text_input("You can type your questions here: ", key="input")
submit = st.button("Ask the question")


if submit:
    response=get_gemini_response(input)
    st.subheader("The Response is")
    st.write(response)

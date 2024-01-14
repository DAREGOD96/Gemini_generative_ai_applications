from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# load the environment variable
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Load the gemini-pro-vision model

def get_response(query, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([query, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# creating streamlit app

st.set_page_config(page_title="Image text extractor")
st.header("Gemini-pro-vision text extractor from image")

query = st.text_input("enter your prompt here:", key="query")
user_uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""

if user_uploaded_file is not None:
    image = Image.open(user_uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Submit")

input_prompt="""
You are an expert in understanding invoices. We will upload a a image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = input_image_details(user_uploaded_file)
    response = get_response(query=query, image=image_data, prompt=input_prompt)
    st.subheader("The Response is")
    st.write(response)

from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# load the env variable

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Load the model

def get_response_from_gemini_pro_vision(query, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([query, image[0], prompt])
    return response.text


def image_data(uploaded_file):
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        image = [
            {
                "mime_type": uploaded_file.type,
                "data": image_bytes
            }
        ]
        return image
    else:
        return "File not found.Please upload the file again"


# initialize the streamlit app

st.set_page_config(page_title="Health app")
st.header("Health app using gemini-pro-vision")
query = st.text_input("please enter your prompt here:", key="query")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

# opening the image using PIL library
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("submit")


# declaring the prompt
prompt = """imagine yourself as a diet specialist.User will provide you a image.From the image you have to tell how 
much calories every item contain. you can use following format as reference 
item 1: this calories, 
item 2: this calories, 
item 3: this calories.... 
you should provide the item name as per user query.if user provide any specific 
item name then only provide that items corresponding calories.
if the provided items is not in the image then you have to say sorry i am unable to fining the item in the photo.
"""

# after clicking the submit button
if submit:
    image_details = image_data(uploaded_file)
    response = get_response_from_gemini_pro_vision(query=query, image=image_details, prompt=prompt)
    st.subheader("The Response is")
    st.write(response)



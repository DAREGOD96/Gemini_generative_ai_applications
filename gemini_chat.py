from dotenv import load_dotenv

load_dotenv()  ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


def get_response_from_genai(query):
    response = chat.send_message(query)

    return response


st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_response_from_genai(query=input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    for chunk in response:
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("Response")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

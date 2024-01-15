from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# load the env variables

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# get response from the generative ai model

def get_response_from_model(query, prompt):
    model = genai.GenerativeModel("gemini-pro")  # loading the gemini pro model
    response = model.generate_content([prompt[0], query])
    return response.text


# function to fetch data using sql query


def fetch_data_from_database(sql, db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(sql)
    results = cur.fetchall()

    for result in results:
        print(result)

    con.commit()
    con.close()
    return results


prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """

]

# initializing the streamlit app

st.set_page_config(page_title="Text_to_Sql_Query")
st.header("Convert text to sql query")
query = st.text_input("enter your query here:", key="query")
submit = st.button("submit")

# if submit is clicked

if submit:
    response = get_response_from_model(query=query, prompt=prompt)
    print(response)
    response = fetch_data_from_database(response, "student.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)


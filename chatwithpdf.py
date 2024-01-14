from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


#load the environment variable
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def get_pdf_text(pdf):
    text=""
    for pdf in pdf:
        pdf_read = PdfReader(pdf)
        for page in pdf_read.pages:
            text += page.extract_text()
    return text


## convert the text into text chunks
def get_text_chunk(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    chunks=text_splitter.split_text(text)
    return chunks


def get_vector_stored(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
    vector_store = FAISS.from_texts(chunks,embedding = embeddings)
    vector_store.save_local("faiss_index")



def get_conversational_chain():

    prompt_template = """
    "Generate comprehensive and easy-to-understand notes on  every topic from the provided context.
    Utilize your own knowledge to supplement information from the document, ensuring clarity and simplicity. 
    Incorporate real-life examples to illustrate key concepts. Generate concise and informative notes , 
    Focus on extracting key concepts, important details, and utilize a structured format with bullet points"\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro",tempareture = 0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables = ['context','question'])
    chain = load_qa_chain(model,chain_type = "stuff",prompt=prompt)

    return chain

def get_user_input (user_query):
    embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
    load_vector = FAISS.load_local("faiss_index",embeddings)
    search = load_vector.similarity_search(user_query)

    chain  = get_conversational_chain()

    response = chain(
        {"input_documents":search, "question": user_query}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with multiple PDF using Gemini💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        get_user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunk(raw_text)
                get_vector_stored(text_chunks)
                st.success("Done")



if __name__ == "__main__":
    main()

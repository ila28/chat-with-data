import streamlit as st

from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


@st.cache_data
def parse_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@st.cache_data
def create_embeddings(text):
    # split into chunks
  text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=0,
    # length_function=len
  )
  chunks = text_splitter.split_text(text)
  
  # create embeddings
  embeddings = OpenAIEmbeddings()
  knowledge_base = FAISS.from_texts(chunks, embeddings, metadatas=[{"source": str(i)} for i in range(len(chunks))])
  return knowledge_base
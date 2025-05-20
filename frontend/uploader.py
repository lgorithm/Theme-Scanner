import streamlit as st
import os
import requests

st.header("📊 Upload Files")
host = os.getenv('HOST')

uploaded_files = st.file_uploader("Upload one or more PDF files:", type=["txt", "pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
# process_url_clicked = st.button("Process Files")
if st.button("Process Files"):
    if uploaded_files:
        files = [("files", file) for file in uploaded_files]
        print(files)
        with st.spinner("Processing Files.."):
            response = requests.post(url=f"{host}/upload/", files=files)
            print(response.json())

import streamlit as st
import os
import requests
import json
from urllib.parse import quote
from streamlit_extras.stylable_container import stylable_container

# Page config
# st.set_page_config(page_title="📂 Uploaded Files", layout="wide")

st.title("📂 Uploaded Files")
st.markdown("Browse and preview your uploaded files below:")

# Fetch files from backend
host = os.getenv('HOST')

try:
    response = requests.get(f"{host}/files")
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"🚨 Error fetching files from backend: {e}")
    st.stop()
except json.JSONDecodeError as e:
    st.error(f"🚨 Error decoding JSON response: {e}")
    st.stop()
except Exception as e:
    st.error(f"🚨 An unexpected error occurred: {e}")
    st.stop()

files = data.get("files", [])

if not files:
    st.info("📭 No files found. Please upload some files.")
else:
    for file in files:
        file_name = file["name"]
        file_type = file["type"]
        file_url = f"{host}/file/{quote(file_name)}"

        with stylable_container(
            key=f"file_{file_name}",
            css_styles="""
                border: 1px solid #eee;
                border-radius: 12px;
                padding: 1.2rem;
                margin-bottom: 1rem;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                background-color: #fafafa;
            """
        ):
            col1, col2 = st.columns([1, 5])
            with col1:
                if file_type == "image":
                    st.image("https://img.icons8.com/ios/50/image.png", width=40)
                elif file_type == "text":
                    st.image("https://img.icons8.com/ios/50/document.png", width=40)
                elif file_type == "pdf":
                    st.image("https://img.icons8.com/ios/50/pdf.png", width=40)
                else:
                    st.image("https://img.icons8.com/ios/50/file.png", width=40)

            with col2:
                st.subheader(file_name)
                if file_type == "image":
                    if st.button(f"🖼️ View Image", key=f"btn_{file_name}"):
                        st.image(file_url, caption=file_name, use_container_width=True)

                elif file_type == "text":
                    if st.button(f"📄 View Text", key=f"btn_{file_name}"):
                        try:
                            text_response = requests.get(file_url)
                            text_response.raise_for_status()
                            st.text_area("File Content", text_response.text, height=300)
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error fetching text file: {e}")

                elif file_type == "pdf":
                    if st.button(f"📑 View PDF", key=f"btn_{file_name}"):
                        st.markdown(
                            f'<iframe src="{file_url}" width="100%" height="700px" style="border: none;"></iframe>',
                            unsafe_allow_html=True
                        )
                else:
                    st.warning(f"📁 Unsupported file type: {file_type}")

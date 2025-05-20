import streamlit as st
from dotenv import load_dotenv

load_dotenv()
uploader_page = st.Page("uploader.py", title="Uploader", icon=":material/upload_file:")
agent_page = st.Page("agent.py", title="Agent", icon=":material/smart_toy:")
documents = st.Page("documents.py", title="Documents", icon=":material/description:")

pg = st.navigation([agent_page, uploader_page, documents])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()
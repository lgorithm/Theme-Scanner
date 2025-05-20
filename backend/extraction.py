from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image
import pytesseract
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from utils import get_file_type

load_dotenv()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1400,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  
)
async def extract(files):
    for file in files:
        type = get_file_type(file['filename'])
        if type == 'pdf':
            try:
                loader = PyPDFLoader(
                    file_path = file['file_path'],
                    mode = "page"
                )
                docs = loader.load()
                print(docs)
                print('Length:', len(docs))
                for doc in docs:
                    doc.metadata["document_id"] = file['filename'].split('.')[0]
                docs = text_splitter.split_documents(docs)
                print('PDF Docs: ', docs)
                print('PDF Extracted Successfully')
                vector_store.add_documents(docs)
                print('PDF data stored in VectorDB')
            except Exception as e:
                print(f"Error: {str(e)}")
        if type == 'image':
            try: 
                image_path = file['file_path'],
                print('Path: ', image_path[0])
                image = Image.open(image_path[0])
                extracted_text = pytesseract.image_to_string(image)
                cleaned_text = extracted_text.strip()
                documents = text_splitter.create_documents(
                    [cleaned_text], 
                    [{'page': 0, 'document_id': file['filename'].split('.')[0]}]
                )
                print('Image Docs: ', documents)
                print('Image Extracted Successfully')
                vector_store.add_documents(documents=documents)
                print('Image data stored in VectorDB')
            except Exception as e:
                print(f"Error: {str(e)}")


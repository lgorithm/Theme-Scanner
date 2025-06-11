from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image
import pytesseract
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from utils import get_file_type
import re
from langchain.schema import Document
                
load_dotenv()
embeddings = OpenAIEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
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
        doc_id = file['filename'].split('.')[0]
        if type == 'pdf':
            try:
                loader = PyPDFLoader(
                    file_path = file['file_path'],
                    mode = "page"
                )
                pages = loader.load()
                print(pages)
                print('Length:', len(pages))
                all_paragraph_docs = []

                for page_num, page_doc in enumerate(pages):
                    full_text = page_doc.page_content.strip()

                    raw_paragraphs = re.split(r'\.\s*\n+|\n\s*\n+', full_text)
                    paragraph_number = 1

                    for para in raw_paragraphs:
                        clean_para = para.strip()
                        if not clean_para:
                            continue
                        metadata = {
                            'document_id': doc_id,
                            'page': page_num + 1,  
                            'paragraph_number': paragraph_number
                        }
                        all_paragraph_docs.append({
                            'content': clean_para,
                            'metadata': metadata
                        })

                        paragraph_number += 1

                vector_store.add_documents([
                    Document(page_content=doc['content'], metadata=doc['metadata'])
                    for doc in all_paragraph_docs
                ])
                print('PDF paragraphs stored in VectorDB')

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
                    [{'page': 1, 'document_id': file['filename'].split('.')[0]}]
                )
                paragraph_number = 1
                for doc in documents:
                    doc.metadata['paragraph_number'] = paragraph_number
                    paragraph_number += 1
                print('Image Docs: ', documents)
                print('Image Extracted Successfully')
                vector_store.add_documents(documents=documents)
                print('Image data stored in VectorDB')
            except Exception as e:
                print(f"Error: {str(e)}")


from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.retrievers.document_compressors import LLMListwiseRerank
from langchain.retrievers import ContextualCompressionRetriever


CHROMA_DIR = "./chroma_langchain_db"
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# Query answer from every documents 
def query_each_document(user_query):
    embedding_model = OpenAIEmbeddings()
    vectordb = Chroma(
        collection_name="example_collection",
        embedding_function=embedding_model,
        persist_directory=CHROMA_DIR,  
    )
    llm = ChatOpenAI(temperature=0.3)

    all_docs = vectordb.get()['metadatas']
    print('Matadata: ', all_docs)
    document_ids = list(set([doc['document_id'] for doc in all_docs]))
    print('doc_id: ', document_ids)
    results = []
    try:
        for doc_id in document_ids:
            retriever = vectordb.as_retriever(
                search_kwargs={
                    "k": 3,
                    "filter": {"document_id": doc_id}
                }
            )
            
            model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

            _filter = LLMListwiseRerank.from_llm(model, top_n=1)
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=_filter, base_retriever=retriever
            )

            combine_docs_chain = create_stuff_documents_chain(
                llm, retrieval_qa_chat_prompt
            )
            retrieval_chain = create_retrieval_chain(compression_retriever, combine_docs_chain)
            result = retrieval_chain.invoke({"input": user_query})
            print("result: ", result)

            doc = result["context"][0]
            meta = doc.metadata
            document_id = meta.get("document_id")
            page = meta.get("page")
            answer = result['answer']
            results.append({
                "document_id": document_id,
                "answer": answer,
                "citations": page
            })

        return results
    except Exception as e:
        print(f"Error: {str(e)}")
        
# Identify multiple themes from answers of different documents
def identify_themes(document_answers):
    llm = ChatOpenAI(temperature=0.2, model="gpt-4")

    formatted_input = "".join([
        f"Document ID: {entry['document_id']} Answer: {entry['answer']}\n"
        for i, entry in enumerate(document_answers)
    ])

    prompt = PromptTemplate.from_template("""
    Given the following responses from different documents, identify 2-5 coherent and recurring themes.
    For each theme, provide:
    - A short descriptive title
    - A concise 2-3 sentence explanation
    - A list of supporting document IDs

    Document Responses:
    {document_answers}

    Format your response clearly.
    """)

    theme_chain = prompt | llm
    themes = theme_chain.invoke({"document_answers": formatted_input})
    return themes

def run_query_and_theme_synthesis(user_query):
    print("\n--- Per-Document Responses ---")
    doc_results = query_each_document(user_query)
    doc_answers = ''
    for entry in doc_results:
        print(f"\nDocument: {entry['document_id']}")
        print(f"Answer: {entry['answer']}")
        print("Citations:", f"Page {entry['citations']}")
        doc_answers += f"Document ID: {entry['document_id']} \n Answer: {entry['answer']}\n Page: {entry['citations']+1}\n\n"

    print("\n--- Document Themes ---")
    themes = identify_themes(doc_results)
    print(themes)
    return doc_answers + '\n' + themes.content


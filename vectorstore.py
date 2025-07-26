import uuid
from langchain_ollama import OllamaEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain_core.documents import Document

vectorstore = Chroma(collection_name="rag_multimodal",embedding_function=OllamaEmbeddings(model="mxbai-embed-large:335m"))
docstore = InMemoryStore()
id_key = "doc_id"


retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    id_key=id_key
)

def store_documents(texts, text_summaries, tables, table_summaries, images, image_summaries):
    doc_ids = [str(uuid.uuid4()) for _ in texts]
    summary_text = [Document(page_content= summary.content, metadata= {id_key:doc_ids[i]}) for i, summary in enumerate(text_summaries)]

    table_ids = [str(uuid.uuid4()) for _ in tables]
    summary_table = [Document(page_content= summary.content, metadata= {id_key:table_ids[i]}) for i, summary in enumerate(table_summaries)]

    image_ids = [str(uuid.uuid4()) for _ in images]
    summary_image = [Document(page_content= summary.content, metadata= {id_key:image_ids[i]}) for i, summary in enumerate(image_summaries)]

    try:
        retriever.vectorstore.add_documents(summary_text)
        retriever.docstore.mset(list(zip(doc_ids, texts)))

        retriever.vectorstore.add_documents(summary_table)
        retriever.docstore.mset(list(zip(table_ids, tables)))

        retriever.vectorstore.add_documents(summary_image)
        retriever.docstore.mset(list(zip(image_ids, images)))
    
    except Exception as e:
        return f"Failed to store documents: {e}"
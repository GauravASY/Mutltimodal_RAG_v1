from unstructured.partition.pdf import partition_pdf
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama



summarization_prompt = """
You are an expert summary generator. 
Your task is to generate concise summaries from the tables and text without losing any important information.
Respond only with summary. No additional comments.
Do not start your message by saying 'Here is the summary' or anything like that.
Just provide the summary as it is
Table or Text : {content}
"""
summary_llm = ChatOllama(model="gemma2:2b")
summarization_prompt_template = ChatPromptTemplate.from_template(summarization_prompt)
summary_chain = summarization_prompt_template | summary_llm

def file_processor(file):
    try :
        document = partition_pdf(
            filename=file,
            strategy="hi_res",
            infer_table_structure=True,
            extract_image_block_to_payload=True,
            extract_image_block_types=["Image"],
            chunking_strategy="by_title",
            #max_characters = 10000,
            #combine_text_under_n_chars = 2000,
            #new_after_n_chars = 5000
        )
        return document
    except Exception as ex:
        raise RuntimeError("PDF processing failed") from ex

def extract_components(docs):
    tables = []
    images = []
    texts = []
    for doc in docs:
        if 'TableChunk' in str(type(doc)):
            tables.append(doc)
        if 'CompositeElement' in str(type(doc)):
            texts.append(doc)
            doc_element = doc.metadata.orig_elements
            for ele in doc_element:
                if "Image" in str(type(ele)):
                    images.append(ele.metadata.image_base64)
    return tables, images, texts

def summarize(texts, tables):
    table_html = [table.metadata.text_as_html for table in tables]
    table_summaries = summary_chain.batch(table_html)
    text_summaries = summary_chain.batch(texts)
    return text_summaries, table_summaries

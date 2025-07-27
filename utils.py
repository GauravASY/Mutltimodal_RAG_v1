from unstructured.partition.pdf import partition_pdf
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



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

image_summarization_prompt = """
You are an expert Image descrition generator.
Your task is to generate detailed description of the Images provided. 
Pay special attention to flow-charts, pie-charts, bar-graphs and other data visualisation techniques. Be specific about them. 
"""

image_llm = ChatOllama(model="llava-phi3")
image_context_msg  = [(
    "user", [
    {'type' : 'text', 'text' : image_summarization_prompt},
    {'type' : 'image_url',  'image_url': {"url": "data:image/jpeg;base64,{base64_image}"},}
])]
image_summarization_prompt_template = ChatPromptTemplate.from_messages(image_context_msg)
image_summary_chain = image_summarization_prompt_template | image_llm


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
    table_summaries = summary_chain.batch(table_html, max_concurrency=3)
    text_summaries = summary_chain.batch(texts, max_concurrency=3)
    return text_summaries, table_summaries


def summarize_images(images):
    image_summaries = image_summary_chain.batch(images, max_concurrency=3)
    return image_summaries

def parse_docs(docs):
    texts = []
    images = []
    for doc in docs:
        if 'CompositeElement' in str(type(doc)):
            texts.append(doc)
        else:
            images.append(doc)
    return {"texts": texts, "images": images}


def build_prompt(args):
    context = args['context']
    query = args['query']
    history = args.get('history', [])

    context_texts= ""
    if len(context['texts']) > 0:
        for text_element in context['texts']:
            context_texts += text_element.text

    human_prompt = [{"type" : "text", "text": f"Context: {context_texts}\nQuestion: {query}"}]
    if len(context['images']) > 0:
            for image in context['images']:
                human_prompt.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})


    system_message = """You are a specialized assistant for answering questions based ONLY on the provided context. Your instructions are to be followed exactly. 
    1. Review the 'Context' below. 
    2. If the 'Context' contains the information to answer the 'Question', provide a helpful answer based solely on that context. 
    3. If the 'Context' does NOT contain the information to answer the 'Question', you MUST respond with the exact phrase: 'I can not process the request'. 
    4. Do NOT use any of your internal knowledge. Do NOT attempt to answer if the information is not in the 'Context' except for greetings."""
    

    prompt = ChatPromptTemplate.from_messages([
    ('system' ,  system_message),
    MessagesPlaceholder(variable_name = "history"),
    ('user' , human_prompt)
])

    final_prompt = prompt.format_messages(history=history)
    return final_prompt
   
    

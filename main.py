import os 
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import gradio as gr
from utils import *
from vectorstore import *

llm = ChatOllama(model="llama3:latest", temperature=0.2)
prompt = ChatPromptTemplate.from_messages([
    ('system' ,  "You are a specialized assistant for answering questions based ONLY on the provided context from PDF documents. Your instructions are to be followed exactly. 1. Review the 'Context' below. 2. If the 'Context' contains the information to answer the 'Question', provide a helpful answer based solely on that context. 3. If the 'Context' does NOT contain the information to answer the 'Question', you MUST respond with the exact phrase: 'I can not process the request'. 4. Do NOT use any of your internal knowledge. Do NOT attempt to answer if the information is not in the 'Context' except for greetings. Context: {context} "),
    MessagesPlaceholder(variable_name = "history"),
    ('user' , '{query}')
])

llm_chain = prompt | llm

def process_query(message, history):
    context = []
    
    for msg in history:
        if msg['role'] == 'user' :
            context.append(HumanMessage(content= msg['content']))
        else :
            context.append(AIMessage(content = msg['content'] ))
    
    chain = prompt | llm
    if len(message['files']) == 0 :
        result = retriever.invoke(message['text'])
        print("\n result :", result)
        yield "Retrieving information from vectorstore..."
    else :
        try:
            for file in message['files']:
                docs = file_processor(file)
                tables, images, texts = extract_components(docs)
                text_summaries, table_summaries = summarize(texts, tables)
                image_summaries = summarize_images(images)
                store_documents(texts, text_summaries, tables, table_summaries, images, image_summaries)
    
            if message['text'].strip() == "" :
                yield "PDF processing successful"
            else :
               result = retriever.invoke(message['text'])
               print("\n result :", result)

        except Exception as e:
            yield f"""Process Failed. {e}"""
    return {"text" : f"You said: {message['text']}"}

def main():
    load_dotenv()
    print("Starting the application...")
    gr.ChatInterface(
        fn=process_query,
        type="messages",
        title="Multimodal PDF R.A.G",
        theme="monochrome",
        description="Ask questions about your PDF documents",
        multimodal=True,
        textbox=gr.MultimodalTextbox(file_count="multiple", file_types=[".pdf"], sources=["upload"])
    ).launch()

if __name__ == "__main__":
    main()

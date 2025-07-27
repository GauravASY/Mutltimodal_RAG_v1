import os 
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import gradio as gr
from utils import *
from vectorstore import *

llm = ChatOllama(model="llama3:latest", temperature=0.2)


def process_query(message, history):
    history_context = []
    
    for msg in history:
        if msg['role'] == 'user' :
            history_context.append(HumanMessage(content= msg['content']))
        else :
            history_context.append(AIMessage(content = msg['content'] ))

    retriever_chain = (
    {
        "context" : lambda x: parse_docs(retriever.invoke(x['query'])),
        "query" : lambda x: x['query'],
        "history" : lambda x: x['history']
    }
    | RunnableLambda(build_prompt) 
    | llm
)
    if len(message['files']) == 0 :
        for result in retriever_chain.stream({
            "query" : message['text'],
            "history" : history_context
        }):
            yield result

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
                for result in retriever_chain.stream({
                    "query" : message['text'],
                    "history" : history_context
                }):
                     yield result

        except Exception as e:
            yield f"""Process Failed. {e}"""

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

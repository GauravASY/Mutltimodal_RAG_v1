import os 
from dotenv import load_dotenv
from unstructured.partition.pdf import partition_pdf
import gradio as gr


def process_query(message, history):
    messages = []
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

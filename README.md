# Advance Multimodal RAG

Multimodal Retrieval-Augmented Generation (RAG) for complex PDF documents using LangChain, ChromaDB, Unstructured,  Gradio, and Ollama.
------

`Disclaimer`:
Since models are run locally, your local machine must meet some hardware specifications. At least 6 GB of available system memory is required. 

## Features

- **PDF Ingestion:** Extracts text, tables, and images from PDF files. 
- **Confidentiality:** Models are run locally, maintaining the confidentiality of sensitive documents.
- **Summarization:** Generates concise summaries for text, tables, and detailed descriptions for images.
- **Multimodal Retrieval:** Stores and retrieves information using vector embeddings and a document store.
- **Question Answering:** Answers user queries based strictly on the provided PDF context.
- **Gradio Interface:** User-friendly chat interface supporting file uploads and multimodal queries.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/rag-multimod.git
   cd rag-multimod
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   Or use the dependencies listed in [pyproject.toml](pyproject.toml).

3. **Extra System dependencies:**
   
   To run locally, Unstructured requires `tesseract-ocr` and `poppler-utils` to be installed on your local machine.
   
   Check official docs for more information: https://docs.unstructured.io/open-source/installation/full-installation

## Usage

Run the application:

```sh
python main.py
```

Open the Gradio interface in your browser, upload PDF files, and ask questions about their content.

## Project Structure

- [`main.py`](main.py): Entry point, Gradio chat interface.
- [`utils.py`](utils.py): PDF processing, summarization, prompt building.
- [`vectorstore.py`](vectorstore.py): Vector storage and retrieval logic.
- [`pyproject.toml`](pyproject.toml): Python dependencies and project metadata.

## Requirements

- Python 3.13+
- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Ollama](https://github.com/ollama/ollama)
- [Gradio](https://github.com/gradio-app/gradio)
- [Unstructured](https://github.com/Unstructured-IO/unstructured)

## Notes

- Only answers questions based on the uploaded PDF context.
- For unsupported queries, responds with: `I can not process the request`.

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Ollama](https://github.com/ollama/ollama)
- [Unstructured](https://github.com/Unstructured-IO/unstructured)

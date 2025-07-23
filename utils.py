from unstructured.partition.pdf import partition_pdf


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
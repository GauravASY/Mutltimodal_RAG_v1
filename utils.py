from unstructured.partition.pdf import partition_pdf


def file_processor(file):
    document = partition_pdf(
        filename=file,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_to_payload=True,
        extract_image_block_types=["Image"],
        chunking_strategy="by_title",
        max_characters = 10000,
        combine_text_under_n_chars = 2000,
        new_after_n_chars = 5000
    )
    return document
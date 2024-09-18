import base64
import os.path
import sys

import replicate
from tqdm import tqdm


def file_to_data_uri(file_path):
    # Read the file
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Encode the file content to base64
    base64_encoded = base64.b64encode(file_content).decode("utf-8")

    # Determine the MIME type (you may need to expand this for other file types)
    file_extension = file_path.split(".")[-1].lower()
    mime_type = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "pdf": "application/pdf",
        # Add more MIME types as needed
    }.get(file_extension, "application/octet-stream")

    # Create the data URI
    data_uri = f"data:{mime_type};base64,{base64_encoded}"

    return data_uri


if __name__ == "__main__":
    pdfs_to_convert = sys.argv[1:]
    for pdf in tqdm(pdfs_to_convert):
        markdown = pdf.replace(".pdf", ".md")
        if os.path.isfile(markdown):
            continue

        output = replicate.run(
            "chigozienri/upload:2472bd8ce171b57576bb610deb154057ad80518fefe7ca059f9e33f073b3456b",
            input=file_to_data_uri(pdf),
        )
        print(output)

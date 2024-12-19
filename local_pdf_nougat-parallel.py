#!/usr/bin/env python3
import base64
import os
import os.path
import random
import sys

import replicate
import requests
from parallelbar import progress_map

# random.seed(42)


def upload_pdf_to_fileio(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Check if the file is a PDF
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("The file must be a PDF.")

    # file.io API endpoint
    url = "https://file.io"

    # Open the file in binary mode
    with open(file_path, "rb") as file:
        # Create a dictionary with the file
        files = {"file": file}

        # Additional parameters
        data = {"expires": "1w"}  # Set expiration to 1 week

        # Send POST request to file.io
        response = requests.post(url, files=files, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        if result["success"]:
            return result["link"]
        else:
            raise Exception("Upload failed: " + result.get("message", "Unknown error"))
    else:
        raise Exception(f"HTTP error occurred: {response.status_code}")


def process_file(pdf):
    markdown = pdf.replace(".pdf", ".md")
    if os.path.isfile(markdown):
        return

    try:
        download_url = upload_pdf_to_fileio(pdf)
        print(f"PDF uploaded successfully. Download URL: {download_url}")

        output = replicate.run(
            "awilliamson10/meta-nougat:872fa99400b0eeb8bfc82ef433aa378976b4311178ff64fed439470249902071",
            input={
                "pdf_link": download_url,
            },
        )
        open(markdown, "w").write(output)
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


if __name__ == "__main__":
    pdfs_to_convert = sys.argv[1:]
    random.shuffle(pdfs_to_convert)

    new_pdfs_to_convert = []
    for pdf in pdfs_to_convert:
        markdown = pdf.replace(".pdf", ".md")
        if os.path.isfile(markdown):
            continue
        else:
            new_pdfs_to_convert.append(pdf)

    #res = progress_map(process_file, new_pdfs_to_convert, n_cpu=32)
    #res = progress_map(process_file, new_pdfs_to_convert, n_cpu=16)
    res = progress_map(process_file, new_pdfs_to_convert, n_cpu=8)

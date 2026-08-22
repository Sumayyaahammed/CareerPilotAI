import os
import fitz


def load_pdf(pdf_path):
    """
    Extract text from a PDF.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def load_knowledge_base(folder_path):
    """
    Load all PDF files from knowledge base.
    """

    documents = []

    for filename in os.listdir(folder_path):

        if filename.lower().endswith(".pdf"):

            file_path = os.path.join(
                folder_path,
                filename
            )

            text = load_pdf(file_path)

            if text.strip():

                documents.append({
                    "source": filename,
                    "text": text
                })

    return documents
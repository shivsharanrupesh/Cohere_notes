import fitz
import cohere
from documents import Documents
from chatbot import Chatbot


def create_parsed_docs(uploaded_files) -> list[dict[str, str]]:
    """
    Parses the uploaded PDF files into a list of dictionaries with title and text as keys

    Params:
        uploaded_files (list[UploadedFile]): the uploaded files (PDFs)

    Returns:
        list[dict[str, str]]: the parsed documents with title and text as keys
    """
    docs = []
    for file in uploaded_files:
        text = ""
        with fitz.open(stream=file.read()) as doc:
            for page in doc:
                text += page.get_text()

        parsed_doc = {"title": file.name, "text": text}
        docs.append(parsed_doc)
    return docs


def init_chatbot(api_key: str, docs: list[dict[str, str]]) -> Chatbot:
    """
    Initializes the chatbot with the given API key and documents

    Params:
        api_key (str): the Cohere API key
        docs (list[dict[str, str]]): the documents to initialize the chatbot with (title and text as keys)

    Returns:
        Chatbot: instance of the chatbot class
    """
    client = cohere.Client(
        api_key=api_key,
    )
    documents = Documents(files=docs, client=client)
    chatbot = Chatbot(docs=documents, client=client)
    return chatbot

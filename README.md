# Class Notes Tutor App - RAG Powered Chabot

## Link
[https://cohere-class-notes.streamlit.app/](https://cohere-class-notes.streamlit.app/)

## Demo
### Cohere API Key required to run this app
https://github.com/ragizaki/CohereClassNotes/assets/43770239/0c80bf86-2a5e-49a9-bc1f-e5bed30e67f7


## Description
I decided to build an RAG-powered chatbot to support connecting to external documents, so that users can upload their class notes as PDF files and ask the chatbot questions
to quickly summarize information. I decided to make this after realizing that the process of finding information in my class notes was taking too long (finding the correct page, searching for the right answer, etc). Instead, you can simply upload all of your class notes to this bot and query information blazingly fast.

The RAG chatbot supports document chunking, embedding, retrieval and reranking, all through [Cohere's APIs](https://cohere.com/). I also built a user-friendly chatbot interface with <b>Streamlit</b> as a way to support PDF uploads. The PDF's are then converted into plaintext strings using the fitz library.

## Tools Used
- Python
- StreamLit
- Cohere Chat and Embedding APIs

## Future
I plan to augment the app to use Cohere's Async client to handle concurrent requests, and also to support multiple tabs for different classes. This way, users can upload their PDF's to different chatbots and keep their different classes organized.

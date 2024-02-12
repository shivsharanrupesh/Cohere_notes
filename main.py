import streamlit as st
from helpers import create_parsed_docs, init_chatbot

st.title("Class Notes Tutor")

# Sidebar
cohere_api_key = st.sidebar.text_input("Enter your Cohere API key", type="password")
st.sidebar.title("Upload class notes")
uploaded_files = st.sidebar.file_uploader(
    "Upload", type="pdf", accept_multiple_files=True
)

docs = []
if uploaded_files:
    docs = create_parsed_docs(uploaded_files)

if not cohere_api_key:
    st.warning("Please enter your Cohere API key")

if not docs:
    st.warning("Please upload some class notes")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if cohere_api_key and docs:
    chatbot = init_chatbot(api_key=cohere_api_key, docs=docs)

    if prompt := st.chat_input("Ask a question about class notes"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # render user message in chat box
        with st.chat_message("user"):
            st.markdown(prompt)

        # render chatbot messages with streaming enabled
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for event in chatbot.generate_response(prompt):
                if event.event_type == "text-generation":
                    full_response += event.text
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

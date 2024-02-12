import uuid


class Chatbot:
    CHAT_PREAMBLE_SEARCH_QUERY = """
        You are a chatbot designed to help students with their class notes.
        Answer questions about class notes formally.
    """
    CHAT_PREAMBLE = """
        You are a chatbot designed to help students with their class notes. Tell the student to ask a question
        about their class notes.
    """

    def __init__(self, docs, client):
        self.docs = docs
        self.client = client
        self.conversation_id = str(uuid.uuid4())

    def generate_response(self, message: str):
        """
        Generate a response from the Cohere chat endpoint for the given message

        Params:
            message (str): the message from the user
        """
        response = self.client.chat(message=message, search_queries_only=True)

        if response.search_queries:
            documents = self.retrieve_docs(response)

            response = self.client.chat(
                message=message,
                documents=documents,
                conversation_id=self.conversation_id,
                preamble_override=self.CHAT_PREAMBLE_SEARCH_QUERY,
                stream=True,
            )

            for event in response:
                yield event

        else:
            response = self.client.chat(
                message=message,
                conversation_id=self.conversation_id,
                stream=True,
                preamble_override=self.CHAT_PREAMBLE,
            )

            for event in response:
                yield event

    def retrieve_docs(self, response) -> list[dict[str, str]]:
        """
        Retrieves the top k documents for a given query (k defaults to self.retrieve_top_k)

        Params:
            response (cohere.Response): the response from the Cohere chat endpoint

        Returns:
            list[dict[str, str]]: the top k documents retrieved, with title and text as keys
        """
        queries = []
        for query in response.search_queries:
            queries.append(query["text"])

        retrieved_docs = []
        for query in queries:
            retrieved_docs.extend(self.docs.retrieve(query))

        return retrieved_docs

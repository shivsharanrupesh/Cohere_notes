from unstructured.partition.text import partition_text
from unstructured.chunking.title import chunk_by_title
import hnswlib


class Documents:
    def __init__(self, files: list[dict[str, str]], client):
        self.files = files
        self.docs = []
        self.docs_embeddings = []
        self.retrieve_top_k = 10
        self.rerank_top_k = 3
        self.client = client

        # loading, embedding and indexing functions
        self.load()
        self.embed()
        self.index()

    def load(self) -> None:
        """
        Loads documents from files and chunks the text content
        """
        for file in self.files:
            elements = partition_text(text=file["text"])
            chunks = chunk_by_title(elements)
            for chunk in chunks:
                self.docs.append({"title": file["title"], "text": str(chunk)})

    def embed(self) -> None:
        """
        Embeds the documents using the Cohere API
        """
        batch_size = 90
        self.docs_len = len(self.docs)

        for i in range(0, self.docs_len, batch_size):
            batch = self.docs[i : min(i + batch_size, self.docs_len)]
            texts = [item["text"] for item in batch]
            docs_embeddings_batch = self.client.embed(texts=texts).embeddings
            self.docs_embeddings.extend(docs_embeddings_batch)

    def index(self) -> None:
        """
        Indexes the documents for fast retrieval using HNSW
        """
        self.index = hnswlib.Index(space="ip", dim=4096)
        self.index.init_index(max_elements=self.docs_len, ef_construction=512, M=64)
        self.index.add_items(
            self.docs_embeddings, list(range(len(self.docs_embeddings)))
        )

    def retrieve(self, query: str) -> list[dict[str, str]]:
        """
        Retrieves the top k documents for a given query (k defaults to self.retrieve_top_k)

        Params:
            query (str): the query to retrieve documents for

        Returns:
            list[dict[str, str]]: the top k documents retrieved, with title and text as keys
        """

        retrieved_docs = []
        query_embedding = self.client.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query",
        ).embeddings

        doc_ids = self.index.knn_query(query_embedding, k=self.retrieve_top_k)[0][0]

        docs_to_rerank = []
        for id in doc_ids:
            docs_to_rerank.append(
                {"title": self.docs[id]["title"], "text": self.docs[id]["text"]}
            )

        rerank_results = self.client.rerank(
            query=query,
            documents=docs_to_rerank,
            top_n=self.rerank_top_k,
            model="rerank-english-v2.0",
        )

        doc_ids_reranked = []
        for doc in rerank_results:
            doc_ids_reranked.append(doc_ids[doc.index])

        for id in doc_ids_reranked:
            retrieved_docs.append(self.docs[id])

        return retrieved_docs

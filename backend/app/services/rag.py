from qdrant_client import QdrantClient

class RAGService:
    def __init__(self, url, api_key, collection="law_docs"):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection

    def upsert_docs(self, docs: list[dict]):
        # each doc: {"id":..., "page_content":..., "metadata": {...}}
        self.client.upsert(
            collection_name=self.collection,
            points=[
                (doc["id"], doc["vector"], doc["metadata"])
                for doc in docs
            ]
        )

    def query(self, vector, top_k=5):
        hits = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            top=top_k
        )
        return hits

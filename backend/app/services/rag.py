from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from app.config import Config

class RAGService:
    def __init__(self, url, api_key, collection=None):
        try:
            self.client = QdrantClient(url=url, api_key=api_key)
            self.collection = collection or Config.COLLECTION_NAME
            self.ensure_collection_exists()  # Add this
        except Exception as e:
            print(f"Error initializing Qdrant client: {e}")
            self.client = None

    def ensure_collection_exists(self):
        """Ensure the collection exists with proper configuration"""
        # First check if client is available
        if self.client is None:
            print("⚠️ Qdrant client not initialized. Skipping collection check.")
            return
            
        try:
            existing_collections = [c.name for c in self.client.get_collections().collections]
            if self.collection not in existing_collections:
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
                )
                print(f"✅ Created collection `{self.collection}`")
            else:
                print(f"ℹ️ Collection `{self.collection}` already exists")
        except Exception as e:
            print(f"Error ensuring collection exists: {e}")

    def upsert_docs(self, docs: list[dict]):
        """Upsert documents to Qdrant"""
        self.ensure_collection_exists()
        
        points = []
        for doc in docs:
            points.append(PointStruct(
                id=doc["id"],
                vector=doc["vector"],
                payload=doc["metadata"]
            ))
        
        try:
            self.client.upsert(
                collection_name=self.collection,
                points=points
            )
            print(f"✅ Upserted {len(points)} documents")
        except Exception as e:
            print(f"Error upserting documents: {e}")
            raise

    def query(self, vector, top_k=5, score_threshold=0.7):
        """Query similar documents with score threshold"""
        try:
            hits = self.client.search(
                collection_name=self.collection,
                query_vector=vector,
                limit=top_k,
                with_payload=True,
                score_threshold=score_threshold
            )
            return hits
        except Exception as e:
            print(f"Error querying documents: {e}")
            return []
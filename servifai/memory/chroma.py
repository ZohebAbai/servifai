import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
load_dotenv()


class ChromaDB:
    def __init__(self, db_dir, oai_org=None):
        self._path = db_dir
        self._oai_org = oai_org
        self._embed = self._get_openai_embeddings()
        self._client_settings = chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(self._path),
            anonymized_telemetry=False,
        )
        self.client = self._get_or_create_db()
        self.collection = self._get_or_create_collection()

    def _get_openai_embeddings(self):
        if 'azure' in self._oai_org:
            return embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                api_base=os.getenv("API_BASE_PATH"),
                api_type="azure",
                model_name="text-embedding-ada-002"
            )
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"
        )

    def _get_or_create_db(self):
        return chromadb.Client(self._client_settings)

    def _get_or_create_collection(self):
        return self.client.get_or_create_collection(
            name=self._path.stem,
            metadata={"hnsw:space": "cosine"},
            embedding_function=self._embed,
        )
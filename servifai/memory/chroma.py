import os

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from llama_index import LangchainEmbedding

load_dotenv()


class ChromaDB:
    def __init__(self, db_dir):
        self._path = db_dir
        self._oai_org = os.getenv("OPENAI_API_TYPE")
        self._client_settings = chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(self._path),
            anonymized_telemetry=False,
        )
        self.embed = self._get_openai_embeddings()
        self.client = self._get_or_create_db()
        self.collection = self._get_or_create_collection()

    def _get_openai_embeddings(self):
        if self._oai_org == "azure":
            return LangchainEmbedding(
                OpenAIEmbeddings(
                    model="text-embedding-ada-002",
                    deployment="text-embedding-ada-002",
                    openai_api_type="azure",
                    openai_api_key=os.getenv("OPENAI_API_KEY"),
                    openai_api_base=os.getenv("OPENAI_API_BASE"),
                    openai_api_version=os.getenv("OPENAI_API_VERSION"),
                ),
                embed_batch_size=1,
            )
        return LangchainEmbedding(
            OpenAIEmbeddings(
                model="text-embedding-ada-002",
                openai_api_key=os.getenv("OPENAI_API_KEY"),
            ),
        )

    def _get_or_create_db(self):
        return chromadb.Client(self._client_settings)

    def _get_or_create_collection(self):
        return self.client.get_or_create_collection(
            name=self._path.stem,
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.embed,
        )

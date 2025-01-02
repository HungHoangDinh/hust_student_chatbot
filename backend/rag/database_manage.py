import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from chunking import Chunking
import requests

class DatabaseManager:
    def __init__(self):
        """Initialize database parameters and setup embedding function."""
        load_dotenv()
        self.database_name = os.environ['DATABASE_NAME']
        self.database_dir = os.environ['DATABASE_DIR']
        self.embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="paraphrase-multilingual-mpnet-base-v2"
        )
        self.client = self._initialize_client()
        self.collection = self._get_or_create_collection()

    def _initialize_client(self):
        """Create the database directory if it doesn't exist and initialize Chroma client."""
        if not os.path.exists(self.database_dir):
            os.mkdir(self.database_dir)
            print("Database directory created successfully.")
        print("create database")

        return chromadb.PersistentClient(path=self.database_dir)

    def _get_or_create_collection(self):
        """Retrieve or create the collection with the specified name and embedding function."""
        print("get or create collection")
        collection = self.client.get_or_create_collection(
            name=self.database_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.embedding_func
        )

        return collection

  
    def add_data(self, data, metadata, id):
        """Add data and corresponding metadata to the collection."""
        if not isinstance(data, list) or not isinstance(metadata, list):
            raise ValueError("Data and metadata should be lists.")
        print("begin add data")
        self.collection.add(documents=data, metadatas=metadata, ids=id)
        print("Data added to the database successfully.")

    def remove_database(self):
        """Remove the collection from the database."""
        self.client.delete_collection(name=self.database_name)
        print("Database collection removed successfully.")


if __name__ == "__main__":
    chunking = Chunking()
    all_data, all_metadata, ids = chunking.chunking_documents()
    db_manage = DatabaseManager()
    db_manage.add_data(data=all_data, metadata=all_metadata, id=ids)

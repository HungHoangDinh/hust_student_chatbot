import json
import time

from chromadb.utils import embedding_functions
import chromadb
import os
from dotenv import load_dotenv
import requests


class Query:
    def __init__(self):
        load_dotenv()
        self.open_api_key = os.environ.get('OPEN_APIKEY')
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

   

    def improve_question(self, question: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.open_api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": """
                        1.Tóm tắt câu hỏi được đưa ra.
                        2. Đưa ra đối tượng tôi cần tìm kiếm từ câu hỏi đó
                        3. Trả kết quả về dạng json chứa hai đối tượng là summary và item, tương ứng với 1 và 2
                        3. Chỉ đưa ra nội dung tôi yêu cầu, không trả lời gì thêm. 
                        4. Không được thêm thông tin gì ngoài ngữ cảnh tôi cung cấp.
                        5. Ví dụ về câu trả lời: {
                                                      "summary": "Mô tả lưu đồ quy trình tiếp nhận yêu cầu VHKT.",
                                                      "item": "Lưu đồ quy trình tiếp nhận yêu cầu VHKT"
                                                    }
                        """}]
                },
                {
                    "role": "user",
                    "content": [{"type": "text",
                                 "text": f'{question}'}]
                }
            ],
            "max_tokens": 4096
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

    def query_collection(self, questions):
        """Get data from vector database"""
        print('Get data from vector database')
        collection_answer = self.collection.query(
            query_texts=questions,
            n_results=10,
        )

        collection_documents = collection_answer['documents']
        collection_distances = collection_answer['distances']
        collection_id = collection_answer['ids']
        documents = []

        for i in range(len(questions)):
            for j in range(len(collection_distances[0])):
                documents.append({'id': collection_id[i][j], 'document': collection_documents[i][j],
                                  'score': collection_distances[i][j]})
        documents_sorted = sorted(documents, key=lambda x: x['score'], reverse=False)
        unique_docs = {}
        top_documents = []

        for doc in documents_sorted:
            if doc['id'] not in unique_docs:
                unique_docs[doc['id']] = doc
                top_documents.append(doc)
            if len(top_documents) == 10:
                break

        return [doc['document'] for doc in top_documents]

    
    def query(self, question):
        try:
            
            question_context = self.improve_question(question=question)
          
            question_context = json.loads(question_context)
            try:
                summary = question_context['summary']
                item = question_context['item']
                questions = [summary, item]
                document = self.query_collection(questions=questions)
           
                return document

            except Exception as err:
                print(f'Error format from answer: {err}')
                return self.query_collection(questions=[question])
            
        except Exception as e:
            print(f"Error when query: {e}")
            return 'Error when query.'


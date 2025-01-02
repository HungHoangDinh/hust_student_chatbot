import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dotenv import load_dotenv
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from ragas.testset import TestsetGenerator

from typing import List  # Thêm dòng này
from langchain.schema import Document  # Để sử dụng Document

def load_markdown_documents(directory: str) -> List[Document]:
    """
    Load all Markdown files with debug information.
    """
    documents = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"Đang xử lý file: {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        doc = Document(
                            page_content=content.strip(),
                            metadata={"source": file_path}
                        )
                        documents.append(doc)
                except Exception as e:
                    print(f"Lỗi khi đọc file {file_path}: {e}")

    return documents

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.environ.get('OPEN_API_KEY')
print('Begin loader')
docs = load_markdown_documents("C:/Users/ASUS/Downloads/support_student_chatbot/backend/rag/md_documents")
print("End loader")
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)
dataset = generator.generate_with_langchain_docs(docs, testset_size=100)
df=dataset.to_pandas()
df.to_csv("dataset.csv", index=False, encoding="utf-8")
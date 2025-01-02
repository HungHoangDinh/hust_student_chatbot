import csv
import ast
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from datasets import Dataset
from ragas import EvaluationDataset
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate
import os
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
csv_file_path = 'final_output.csv'

os.environ["OPENAI_API_KEY"] = os.environ.get("OPEN_API_KEY")
datalist = []

# Đọc file CSV và chuyển đổi dữ liệu
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Tạo một từ điển cho từng hàng
        data = {
            'question': row.get('question', '').strip(),
            'ground_truths': (ast.literal_eval(row.get('ground_truths', '')))[0],
            'answer': row.get('answer', '').strip(),
            'contexts':  row.get('contexts', '').strip(),
        }
        datalist.append(data)
        retrived=[]
        for item in datalist:
            retrived.append([item['contexts']])
        dataset_dict = {
            'user_input': [item['question'] for item in datalist],
            'reference': [item['ground_truths'] for item in datalist],
            'response': [item['answer'] for item in datalist],
            'retrieved_contexts': retrived,
        }

        dataset = Dataset.from_dict(dataset_dict)

eval_dataset = EvaluationDataset.from_hf_dataset(dataset)
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
metrics = [
    LLMContextRecall(llm=evaluator_llm),
    FactualCorrectness(llm=evaluator_llm),
    Faithfulness(llm=evaluator_llm),
    SemanticSimilarity(embeddings=evaluator_embeddings)
]
results = evaluate(dataset=eval_dataset, metrics=metrics)
df = results.to_pandas()
df.to_excel('final_eval.xlsx', index=False)
df.head()
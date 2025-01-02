import requests
import json
import requests
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
class Agent:
    def __init__(self):
        load_dotenv()
        self.open_api_key=os.environ['OPEN_API_KEY']
    def question_classification(self, question: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.open_api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": (
                        "1.Đọc câu hỏi mà tôi đưa ra.\n"
                        "2. Xác định câu hỏi được đưa ra có phải câu chào hỏi thông thường (để làm quen, giới thệu) hay không\n"
                        "3. Nếu là câu chào hỏi thông thường, hãy trả lời là 'false'\n"
                        "3. Nếu là câu hỏi về kiến thức, hãy trả về 'true'\n"
                        "4. Chỉ trả lời là 'true' hoặc 'false'\n"
                        "5. Không được thêm thông tin gì ngoài ngữ cảnh tôi cung cấp"
                    )}]
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

    def get_answer_local_graph(self, question:str):
        try:
            local_graph_url = "http://localhost:8000/local/query/"
            
            data = {"question": question}
            response = requests.post(local_graph_url,params=data )
            
            response.raise_for_status() 
            result = response.json()
            return result['result']
        except Exception as e:
            print(e)
            return  ""
    def get_answer_global_graph(self, question:str):
        try:
            global_graph_url = "http://localhost:8000/global/query"
            
            data = {"question": question}
            response = requests.post(global_graph_url,params=data )
            response.raise_for_status() 
            
            result = response.json()
          
            return result['result']
        except Exception as e:
            print(e)
            return  ""
    def get_answer_rag(self, question:str):
        try:
            rag_url="http://localhost:5000/query_collection"
            headers = {"Content-Type": "application/json"}
            data = {"question": question}
            response = requests.post(rag_url, json=data, headers=headers)
            response.raise_for_status() 
            result = response.json()
            return result['result'] 
        except Exception as e:
            print(e)
            return ""
    def query_greeting(self, question):
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
                                1. Bạn đang đóng vai trò là một chatbot của Đại học Bách khoa Hà Nội.
                                2. Bạn được xây dựng bởi Sinh viên Hoàng Đình Hùng, dưới sự hướng dẫn của Tiến sỹ Trần Nhật Hóa.
                                3. Bạn được xây dựng để trả lời các câu hỏi liên quan đến các quy định, quy chế của Đại học Bách khoa Hà Nội.
                                4. Đứng trên các vai trò trên, bạn hãy trả lời câu chào hỏi dưới đây khi người dùng gặp bạn.
                                5. Trả lời bằng tiếng việt.
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

    def query_from_chatgpt(self, question, info, histories=None):
        messages = [
            {
                "role": "system",
                "content": [dict(type="text", text="""
                1. Trả lời bằng tiếng việt.
                2. Đọc câu hỏi của user và câu trả lời của assistant được cung cấp.
                3. Đọc câu hỏi được đưa ra. Trả lời thông tin dựa trên câu hỏi của user, câu trả lời của assistant trước đó và thông tin được cung cấp ngay phía sau câu hỏi.
                4. Trả lời chi tiết nhất có thể.
                5. Nếu không có thông tin được cung cấp thì trả lời là "Không tìm thấy dữ liệu về câu hỏi", đừng cung cấp thông tin không được tôi đề cập """)]
            }
        ]
        if histories:
            for history in histories:
                messages.append({
                    "role": history["role"],
                    "content": [{'type': "text",
                                 "text": history['content']}]
                })
        messages.append({
            "role": "user",
            "content": [{"type": "text",
                         "text": f' Câu hỏi: {question}, Thông tin liên quan:{info}'}]
        })

        

        client = OpenAI(api_key=self.open_api_key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    def query(self, question):
        try:
            question_type = self.question_classification(question=question)

            if question_type == "true":
                with ThreadPoolExecutor() as executor:
                    # future_local = executor.submit(self.get_answer_local_graph, question=question)
                    future_rag = executor.submit(self.get_answer_rag, question=question)
                    
                    try:
                        # local_graph_answer = future_local.result()
                        rag_answer = future_rag.result()
                        
                        answer =(f"Văn bản 1: {rag_answer}. ")
                                # f"Văn bản 2: {global_graph_answer}. "
                                # f"Văn bản 2: {rag_answer}.")
                        for chunk in self.query_from_chatgpt(question=question, info=answer):
                         
                            yield chunk
                    except Exception as err:
                        print(f'Error format from answer: {err}')
                        yield 'Error format from answer'
                        
            else:
                answer = self.query_greeting(question=question)
                yield answer
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            yield f"Unexpected error: {str(e)}"

    

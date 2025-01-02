import requests
import json
import requests
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys,csv,asyncio
answer_list = []
contexts_list = []
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
            print(response)
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
        print(response.json().get('choices', [{}])[0].get('message', {}).get('content', ''))
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

    def query_from_chatgpt(self, question, info, histories=None):
        """
        Struct of histories: a array of question and answer of system.
        Example: histories=[
                    {"role": "user", "content": "message 1 content."},
                    {"role": "assistant", "content": "message 2 content"},
                    {"role": "user", "content": "message 3 content"},
                    {"role": "assistant", "content": "message 4 content."},
                    {"role": "user", "content": "message 5 content."}
                     ],
        """

        messages = [
            {
                "role": "system",
                "content": [dict(type="text", text="""
                1. Trả lời bằng tiếng việt.
                2. Đọc câu hỏi của user và câu trả lời của assistant được cung cấp.
                3. Đọc câu hỏi được đưa ra. Trả lời thông tin dựa trên câu hỏi của user, câu trả lời của assistant trước đó và thông tin được cung cấp ngay phía sau câu hỏi.
                4. Nếu không có thông tin được cung cấp thì trả lời là "Không tìm thấy dữ liệu về câu hỏi", đừng cung cấp thông tin không được tôi đề cập """)]
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

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.open_api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "max_tokens": 4096
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

    def query(self, question):
        try:
            question_type = self.question_classification(question=question)

            if question_type == "true":
                # Khởi tạo ThreadPoolExecutor để chạy ba hàm song song
                with ThreadPoolExecutor() as executor:
                    # Gửi các hàm tới executor và gán kết quả vào tương lai (future)
                    future_local = executor.submit(self.get_answer_local_graph, question=question)
                    future_rag = executor.submit(self.get_answer_rag, question=question)
                    
                    # Đợi cả ba tương lai hoàn thành và lấy kết quả
                    try:
                        local_graph_answer = future_local.result()
                        rag_answer = future_rag.result()
                        
                        answer =(f"Văn bản 1: {local_graph_answer}. "
                                
                                f"Văn bản 2: {rag_answer}.")
                        result= self.query_from_chatgpt(question=question, info=answer)
                        answer_list.append(result)
                        contexts_list.append(answer)
                        return result
                    except Exception as err:
                        print(f'Error format from answer: {err}')
                        return 'Error format from answer'
                        
            else:
                answer = self.query_greeting(question=question)
                answer_list.append(answer)
                contexts_list.append("")
                return answer
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"Unexpected error: {str(e)}"

if __name__ == '__main__':
    answer_list.clear()
    contexts_list.clear()
    agent=Agent()
    

    with open("output_questions_answers.csv", mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        next(csv_reader)
        output_data = []
        for row in csv_reader:
            question = row[0]
            escaped_question = question.replace('"', '\\"').replace("'", "\\'")
            ground_truth = row[1]
            ground_truths = [ground_truth]
            agent.query(question=question)
            answer = answer_list[-1] if answer_list else "No answer"
            context = contexts_list[-1] if contexts_list else "No context"
            output_data.append({
                'question': question,
                'ground_truths': ground_truths,
                'answer': answer,
                'contexts': context
            })


        with open('final_output.csv', mode='w', newline='', encoding='utf-8') as output_file:
            fieldnames = ['question', 'ground_truths', 'answer', 'contexts']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            # Write the rows
            for data in output_data:
                writer.writerow(data)

        print("Data has been written to final_output.csv")



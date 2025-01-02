import csv
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
open_api_key = os.environ.get('OPEN_API_KEY')

client = OpenAI(api_key=open_api_key)

question_pattern = r"Câu hỏi: (.*?),"
answer_pattern = r"Trả lời: (.*)"


def process_csv(input_file, output_file):
    # Mở file CSV đầu vào và đọc
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile)

        # Mở file CSV đầu ra để ghi
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            csv_writer = csv.writer(outfile)

            csv_writer.writerow(['question', 'answer'])

            next(csv_reader)

            for row in csv_reader:
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "developer",
                         "content": "Tôi cung cấp cho bạn 1 đoạn văn trong đó có cả câu hỏi và ngữ cảnh. Sinh cho tôi câu hỏi và câu trả lời tương ứng bằng tiếng việt."
                                    "Bạn phải trả về theo định dạng sau: {Câu hỏi: Hà Nội là gì, Trả lời: Hà Nội là thủ đô của việt nam}. Giữ câu hỏi và trả lời phải ngăn cách nhau bởi dấu phẩy"
                                    "Câu trả lời phải dựa trên ngữ cảnh tôi cung cấp, bạn không được phép thêm vào bất kỳ thông tin gì"},
                        {"role": "user", "content": f"{row}"}
                    ]
                )
                print(completion.choices[0].message)
                message = completion.choices[0].message.content

                question = re.search(question_pattern, message).group(1)
                answer = re.search(answer_pattern, message).group(1)

                csv_writer.writerow([question, answer])


process_csv('dataset.csv', 'output_questions_answers.csv')

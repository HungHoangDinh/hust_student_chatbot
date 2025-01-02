import os
import requests
from dotenv import load_dotenv
from langchain_text_splitters import MarkdownHeaderTextSplitter


class Chunking:
    def __init__(self, document_path='./md_documents',
                 context="Trả lời bằng tiếng việt, đưa ra một đoạn tổng hợp ngắn."):
        # Load environment variables
        load_dotenv()
        self.open_api_key = os.environ.get('OPEN_APIKEY')
        self.document_path = document_path
        self.context = context

    def _get_summary(self, content):
        """Summarize the content using OpenAI's API."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.open_api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": self.context}]
                },
                {
                    "role": "user",
                    "content": [{"type": "text",
                                 "text": f'Mô tả ngắn gọn nội dung sau, ngoài ra không trả lời gì thêm: {content}'}]
                }
            ],
            "max_tokens": 4096
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', '')

    def _split_and_summarize_document(self, filename):
        """Read and split a Markdown document, then summarize each section."""
        data = []
        metadata = []

        with open(f"{self.document_path}/{filename}", 'r', encoding='utf-8') as file:
            markdown_document = file.read()

        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3"), ("####", "Header 4")]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(markdown_document)

        for md_header_split in md_header_splits:
            content = md_header_split.page_content
            mts = md_header_split.metadata
            for mt in mts:
                content = f"{mts[mt]}. {content}"

            content = f"{filename[:-3]}. {content}"
            summary_content = self._get_summary(content=content)
            content_with_summary = f"{content}. Nội dung chính của đoạn này là: {summary_content}"

            data.append(content_with_summary)
            mts['summary'] = summary_content
            metadata.append(mts)

        return data, metadata

    def chunking_documents(self):
        """Process all Markdown documents in the specified directory."""
        all_data = []
        all_metadata = []
        for filename in os.listdir(self.document_path):
            print(f"Chunking file {filename}")
            if filename.endswith('.md'):
                data, metadata = self._split_and_summarize_document(filename)
                all_data.extend(data)
                all_metadata.extend(metadata)
        ids=list(range(1,len(all_data)+1));
        ids_string_array = [str(i) for i in ids]
        return all_data, all_metadata,ids_string_array

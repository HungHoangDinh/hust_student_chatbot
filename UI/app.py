import streamlit as st
import requests
from PIL import Image
import time
from charset_normalizer import detect

logo = Image.open("images/hust.png")
st.set_page_config(page_title="HUST CHATBOT",page_icon=logo)
def get_answer(question):
    response = requests.post(
        "http://localhost:3000/query",
        params={"question": question},
        headers={"Content-Type": "application/json"},
        stream=True  # Stream response to handle chunks
    )
    
    if response.status_code != 200:
        yield f"Request failed with status code {response.status_code}"
        return

    for chunk in response.iter_content(chunk_size=1024):  # Adjust chunk size as needed
        if chunk is not None:
            try:
                # Attempt to decode the chunk
                decoded_chunk = chunk.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to automatic encoding detection
                encoding_result = detect(chunk)
                encoding = encoding_result.get('encoding', 'utf-8')  # Default to UTF-8
                try:
                    decoded_chunk = chunk.decode(encoding)
                except UnicodeDecodeError as e:
                    yield f"Error decoding chunk with encoding {encoding}: {e}"
                    continue
            
            yield decoded_chunk
        time.sleep(0.05)

with st.sidebar:
    st.title('HUST CHATBOT')
    
    st.sidebar.write("**SVTH:** Hoàng Đình Hùng")
    st.sidebar.write("**MSSV:** 20210399")
    st.sidebar.write("**GVHD:** TS. Trần Nhật Hóa")
    st.sidebar.write("**Email:** Hung.HD210399@sis.hust.edu.vn")
    st.write("")  
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("Trợ lý ảo được xây dựng với mục đích hỗ trợ sinh viên ĐHBKHN hỏi đáp quy định, quy chế của đại học.") 

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập nội dung câu hỏi?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        response=st.write_stream(get_answer(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})

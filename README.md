# Chatbot tư vấn quy định / quy chế cho sinh viên ĐHBKHN

Trợ lý ảo được xây dựng với mục đích hỗ trợ sinh viên ĐHBKHN hỏi đáp quy định, quy chế của đại học.
---

## 📌 Mục Tiêu Của Ứng Dụng

1. **Trả lời được các quy định/ quy chế có trong cơ sở dữ liệu:**
    - Xử lý các văn bản được đưa vào hệ thống.
    - Trả lời phản hồi người dùng từ những thông tin trong hệ thống có.

2. **Tránh tình trạng ảo giác(hallucination):**
    - Có cơ chế để hạn chế được tình trạng ảo giác(hallucination) vốn có của các mô hình ngôn ngữ lớn.

3. **Xử lý bài toán quy chế cho nhiều khóa sinh viên khác nhau:**
    - Nghiên cứu GraphRag để hiểu thông tin nhiều hơn và hiểu được nội dung nào được giành cho khóa nào.

4. **Có giao diện tương tác người dùng:**
    - Xây dựng giao diện streamlit.
    - Tương tác với server thông qua các API.

---

## 🚀 Hướng Dẫn Cài Đặt và Sử Dụng

Dự án được chia thành bốn phần chính: **GraphRag**, **Rag**, và **Agent** và **UI**. Dưới đây là hướng dẫn chi tiết cho từng phần.

---

### **1. RAG**

#### **Yêu cầu:**
- Python phiên bản >= 8.0
- Môi trường máy ảo Anaconda.

#### **Hướng dẫn:**
1. Điều hướng đến thư mục `backend/rag`:
   ```bash
   cd backend
   cd rag
    ```
2. Cài đặt các dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Tạo file .env với các tham số như trong file env.example
4. Chạy server với python:
    ```bash
    python app.py
    ```
### **2.  GraphRag**
#### **Yêu cầu:**
- Python phiên bản >= 8.0
- Môi trường máy ảo Anaconda.

#### **Hướng dẫn:**
1. Điều hướng đến thư mục `backend/graphrag`:
   ```bash
   cd backend
   cd graphrag
    ```
2. Cài đặt các dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Tạo file .env với các tham số như trong file env.example

4. Chạy server với python:
    ```bash
    python app.py
    ```
### **3. Agent**
#### **Yêu cầu:**
- Python phiên bản >= 8.0
- Môi trường máy ảo Anaconda.

#### **Hướng dẫn:**
1. Điều hướng đến thư mục `backend/agent`:
   ```bash
   cd backend
   cd agent
    ```
2. Cài đặt các dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Tạo file .env với các tham số như trong file env.example
4. Chạy server với python:
    ```bash
    python app.py
    ```
### **4. UI**
#### **Yêu cầu:**
- Python phiên bản >= 8.0
- Môi trường máy ảo Anaconda.

#### **Hướng dẫn:**
1. Điều hướng đến thư mục `UI`:
   ```bash
   cd UI
    ```
2. Cài đặt các dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Chạy giao diện với streamlit:
    ```bash
    streamlit run app.py
    ```

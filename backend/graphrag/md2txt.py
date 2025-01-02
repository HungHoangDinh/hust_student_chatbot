import os

input_dir = "../rag/md_documents"
output_dir = "ragtest/input"  

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".md"):  
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".md", ".txt"))
        
        with open(input_path, "r", encoding="utf-8") as infile:
            content = infile.read()
        
        with open(output_path, "w", encoding="utf-8") as outfile:
            outfile.write(content)
        
        print(f"Đã chuyển đổi: {filename} -> {os.path.basename(output_path)}")

print("Hoàn tất chuyển đổi tất cả các file .md sang .txt.")

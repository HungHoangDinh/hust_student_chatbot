from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os 
app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/global/query")
def query_rag_global(question: str):
    try:
        command = ["python", "-m", "graphrag.query", "--root", "./ragtest", "--method", "global", question]
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

 
        result = subprocess.run(command, capture_output=True, text=True,encoding="utf-8", env=env)
        result_text = result.stdout

        start_index = result_text.find("Global Search Response:")
        if start_index != -1:
            global_search_response = result_text[start_index + len("Global Search Response:"):].strip()
        else:
            global_search_response = "Global Search Response not found."
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {result.stderr}")

        return {"result": global_search_response}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/local/query")
def query_rag_local(question: str):
    print(question)
    try:
        command = ["python", "-m", "graphrag.query", "--root", "./ragtest", "--method", "local", question]
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

 
        result = subprocess.run(command, capture_output=True, text=True,encoding="utf-8", env=env)
        result_text = result.stdout
        print(result_text)
        start_index = result_text.find("Local Search Response:")
        if start_index != -1:
            local_search_response = result_text[start_index + len("Local Search Response:"):].strip()
        else:
            local_search_response = "Local Search Response not found."
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {result.stderr}")

        return {"result": local_search_response}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

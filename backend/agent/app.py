from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
from agent import Agent
import requests
import sys
from fastapi.responses import StreamingResponse
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()
agent_instance=Agent()


@app.post("/query")
def query_rag(question: str):
    try:
        async def stream_rag_answer():
            try:
             
                for chunk in agent_instance.query(question=question):
                    
                  
                    yield chunk  
            except Exception as e:
                yield f"Error: {str(e)}"  

        return StreamingResponse(stream_rag_answer(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)

import json
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
from query import Query
app = FastAPI()
query_instance = Query()

class QueryRequest(BaseModel):
    question: str
@app.post("/query_collection")
def query_collection(data: QueryRequest):
    try:
        data_answer=query_instance.query(data.question)
        return {'result': ".  ".join(data_answer)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
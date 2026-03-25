# Integration Guide

LLM Guard is designed to be a lightweight middleware layer in any LLM pipeline.

## 1. FastAPI Middleware Example

```python
from fastapi import Request
from .app.main import evaluate_text

async def llm_guard_middleware(request: Request, call_next):
    body = await request.json()
    if "text" in body:
        eval_res = await evaluate_text(body["text"])
        if eval_res.verdict == "BLOCKED":
            return JSONResponse(status_code=400, content={"error": "Safety violation detected"})
    return await call_next(request)
```

## 2. LangChain Chain Integration

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

def safe_chain(input_text: str):
    # Guard Check
    guard = httpx.post("http://localhost:7860/api/v1/guard", json={"text": input_text}).json()
    if guard["verdict"] == "BLOCKED":
        return "Internal Safety Error"
    
    # Process if safe
    llm = ChatOpenAI()
    return llm.invoke(input_text)
```

## 3. Standalone HTTP Client (Python)

```python
import httpx

def check_safety(text: str):
    with httpx.Client() as client:
        response = client.post("http://localhost:7860/api/v1/guard", json={"text": text})
        return response.json()
```

from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from .schemas import GuardRequest, BatchGuardRequest, GuardResponse
from .guard import LLMGuard
from .rag_engine import RAGEngine
import uuid
import time
import json

app = FastAPI(
    title="RiskOS LLM Guard",
    description="RAG-augmented LLM output guardrail system",
    version="1.0.0"
)

# Initialize components
guard = LLMGuard()
rag = RAGEngine()

@app.post("/api/v1/guard", response_model=GuardResponse)
async def evaluate_text(request: GuardRequest):
    """Evaluate a single text for safety"""
    # 1. RAG-augmented policy lookup (if context or text suggests specific policy)
    relevant_policies = rag.find_relevant_policies(request.text)
    
    # 2. Run guard evaluation
    result = guard.evaluate(request.text, context=request.context)
    
    # Update RAG context flag
    if relevant_policies:
        result["rag_context_used"] = True
        
    return result

@app.post("/api/v1/guard/batch", response_model=List[GuardResponse])
async def evaluate_batch(request: BatchGuardRequest):
    """Evaluate a batch of texts for safety"""
    results = []
    for text in request.texts:
        results.append(guard.evaluate(text))
    return results

@app.get("/api/v1/policies")
async def list_policies():
    """List all active safety policies"""
    return {"policies": rag.policies}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "llm-guard"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

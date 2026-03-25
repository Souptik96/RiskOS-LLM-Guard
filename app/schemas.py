from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GuardRequest(BaseModel):
    text: str = Field(..., description="The LLM output or user input to evaluate")
    context: Optional[str] = Field(None, description="Optional RAG context or user query context")
    user_id: Optional[str] = Field("anonymous", description="User identifier for tracking")

class BatchGuardRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to evaluate in batch")

class GuardResponse(BaseModel):
    guard_id: str
    input_text: str
    verdict: str  # SAFE, FLAGGED, BLOCKED
    reason: str
    policy_triggered: Optional[str] = None
    rag_context_used: bool = False
    confidence: float = 1.0
    latency_ms: float = 0.0

class Policy(BaseModel):
    id: str
    name: str
    description: str
    severity: str  # high, medium, low
    action: str  # block, flag
    examples: List[str]

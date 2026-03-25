import os
import re
from typing import Dict, Any, List, Optional
import time
import uuid

class LLMGuard:
    def __init__(self):
        # Fallback keywords for basic safety if APIs are down
        self.block_keywords = [
            "bomb", "nuclear", "explosive", "weapon", "gun", "drugs", "stolen",
            "credit card", "ssn", "social security", "ethnic cleansing",
            "child sexual", "assassinate", "kill myself", "hate speech", "harassment"
        ]
        self.jailbreak_keywords = ["ignore initial instructions", "disregard safety", "DAN mode"]

    def evaluate(self, text: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Evaluate text against safety policies"""
        start_time = time.time()
        
        # 1. PII Detection (Basic Regex)
        pii_hits = self._detect_pii(text)
        if pii_hits:
            return self._result(text, "BLOCKED", f"PII Detected: {', '.join(pii_hits)}", "PII_LEAKAGE", start_time)

        # 2. Keyword Safety Check
        safety_hits = self._check_keywords(text)
        if safety_hits:
            return self._result(text, "BLOCKED", f"Unsafe content detected: {', '.join(safety_hits)}", "HARMFUL_CONTENT", start_time)

        # 3. Jailbreak Detection
        jb_hits = self._check_jailbreak(text)
        if jb_hits:
            return self._result(text, "BLOCKED", "Potential jailbreak attempt detected", "JAILBREAK_PREVENTION", start_time)

        # Default: Safe
        return self._result(text, "SAFE", "All checks passed", None, start_time, confidence=0.98)

    def _detect_pii(self, text: str) -> List[str]:
        hits = []
        # Email
        if re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text):
            hits.append("Email Address")
        # SSN (Simple 000-00-0000)
        if re.search(r'\d{3}-\d{2}-\d{4}', text):
            hits.append("Social Security Number")
        # Credit Card (Basic 16 digit)
        if re.search(r'\d{4}-\d{4}-\d{4}-\d{4}', text) or re.search(r'\d{16}', text):
            hits.append("Credit Card Number")
        return hits

    def _check_keywords(self, text: str) -> List[str]:
        lower_text = text.lower()
        return [k for k in self.block_keywords if k in lower_text]

    def _check_jailbreak(self, text: str) -> List[str]:
        lower_text = text.lower()
        return [k for k in self.jailbreak_keywords if k in lower_text]

    def _result(self, text: str, verdict: str, reason: str, policy: Optional[str], start_time: float, confidence: float = 1.0) -> Dict[str, Any]:
        return {
            "guard_id": str(uuid.uuid4()),
            "input_text": text,
            "verdict": verdict,
            "reason": reason,
            "policy_triggered": policy,
            "rag_context_used": False,
            "confidence": confidence,
            "latency_ms": round((time.time() - start_time) * 1000, 2)
        }

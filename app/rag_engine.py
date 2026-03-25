import json
import os
from typing import List, Dict, Any

class RAGEngine:
    def __init__(self, policy_path: str = "app/policies/default_policies.json"):
        self.policy_path = policy_path
        self.policies = self._load_policies()

    def _load_policies(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.policy_path):
            with open(self.policy_path, "r") as f:
                return json.load(f)
        return []

    def find_relevant_policies(self, text: str) -> List[Dict[str, Any]]:
        """
        Find relevant policies based on keyword matching (baseline for RAG).
        In a real RAG system, this would use semantic embeddings.
        """
        relevant = []
        lower_text = text.lower()
        
        for policy in self.policies:
            # Check description or examples for overlap
            if any(example.lower() in lower_text for example in policy.get("examples", [])):
                relevant.append(policy)
            elif any(word in lower_text for word in policy["description"].lower().split()):
                relevant.append(policy)
        
        return relevant

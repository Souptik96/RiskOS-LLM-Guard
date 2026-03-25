# LLM Guard Policies

LLM Guard uses a semantic policy retrieval system to identify and enforce safety boundaries.

## 1. Default Policy Schema

Each policy is defined in `app/policies/default_policies.json` with the following structure:
```json
{
    "id": "POLICY_ID",
    "name": "Human Name",
    "description": "Behavioral boundary description",
    "severity": "high | medium | low",
    "action": "block | flag",
    "examples": ["Triggering input 1", "Triggering input 2"]
}
```

## 2. Default Policies

| Policy ID | Name | Target | Severity |
|---|---|---|---|
| `JAILBREAK_PREVENTION` | Jailbreak Prevention | Instruction override attempts | High |
| `PII_LEAKAGE` | PII Leakage | Exposure of private data (SSN, Email) | High |
| `HARMFUL_CONTENT` | Harmful Content | Dangerous/Illegal instructions | High |
| `PROMPT_INJECTION` | Prompt Injection | Malicious data-to-instruction conversion | Medium |
| `SYSTEM_PROMPT_RECOVERY` | System Prompt Extraction | Leaking internal configuration | Medium |

## 3. Severity Levels

- **HIGH**: Transaction is immediately `BLOCKED`. A reason is cited and a fallback response is recommended.
- **MEDIUM**: Depending on confidence, the result is either `BLOCKED` or `FLAGGED`.
- **LOW**: The result is `FLAGGED` and logged to Opik for manual audit, but the generation may still pass through.

## 4. Custom Policies

To add a custom policy:
1. Open `app/policies/default_policies.json`.
2. Add a new object following the schema.
3. Restart the service to refresh the RAG index.

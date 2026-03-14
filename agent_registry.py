from prompts import CFO_PROMPT, COMPLIANCE_PROMPT, OPS_PROMPT, EVANGELIST_PROMPT

AGENTS = {
    "CFO": {
        "persona": CFO_PROMPT,
        "domain": "financial"
    },
    "COMPLIANCE": {
        "persona": COMPLIANCE_PROMPT,
        "domain": "compliance"
    },
    "OPERATIONS": {
        "persona": OPS_PROMPT,
        "domain": "operational"
    },
    "EVANGELIST": {
        "persona": EVANGELIST_PROMPT,
        "domain": "strategic"
    }
}

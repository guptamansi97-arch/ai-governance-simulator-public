# Governance Agent Personas

The simulator utilizes four distinct AI agents, each programmed with a unique professional bias and specific evaluation criteria.

## 1. The Chief Financial Officer (CFO)
- **Primary Bias**: Conservative Capital Preservation.
- **Focus Areas**: Budget exposure, timeline realism, ROI clarity, and financial fragility under stress.
- **Tone**: Skeptical but pragmatic; seeks to minimize downside.

## 2. The Compliance Officer
- **Primary Bias**: Regulatory Integrity and Risk Containment.
- **Focus Areas**: Data governance, regulatory adherence, third-party processing, and audit readiness.
- **Tone**: Formal and cautious; focused on legal defensibility.

## 3. The Operations Lead
- **Primary Bias**: Execution Feasibility and Stability.
- **Focus Areas**: Implementation timeline, workflow integration, process disruption, and resource availability.
- **Tone**: Practical and skeptical of over-promising; focused on day-to-day stability.

## 4. The AI Evangelist
- **Primary Bias**: Strategic Opportunity and Innovation.
- **Focus Areas**: Competitive advantage, future-proofing, market relevance, and innovation upside
- **Tone**: Optimistic and visionary; challenges overly conservative stances when the strategic benefit is material.


## Agent Registry
Agents are centrally registered in `agent_registry.py`. This registry maps agent identifiers to their specific persona prompts and professional domains.

```python
AGENTS = {
    "CFO": {
        "persona": CFO_PROMPT,
        "domain": "financial"
    },
    "COMPLIANCE": {
        "persona": COMPLIANCE_PROMPT,
        "domain": "compliance"
    },
    ...
}
```

## Adding a New Agent
To add a new agent to the simulation:
1. Define the agent's persona prompt in `prompts.py`.
2. Add the agent to the `AGENTS` dictionary in `agent_registry.py`.
3. Specify the agent's `domain` (e.g., "financial", "compliance", "legal", "security") to ensure correct risk mapping in the final report.

The simulation engine will automatically include the new agent in the bulk evaluations (Rounds 1 and 3) and the sequential focal-led debate (Round 2).

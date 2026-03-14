# System Architecture

The AI Governance Stress Test Simulator is built on a modular Python architecture designed for scalability, transparency, and ease of use in both CLI and Web environments.

## Component Overview

### 1. Central Orchestration (`engine.py`)
The `SimulationEngine` is the heart of the system. It manages:
- Sequential execution of the three simulation rounds.
- Triggering metrics computation.
- Consolidating results into executive reports.
- Progress reporting via callbacks.
- Persistence of outputs and index management.

### 2. Reasoning Engine (`simulation.py` & `agents.py`)
This layer handles the multi-agent debate logic.
- **Dynamic Agents**: Supports any number of agents defined in `agent_registry.py`.
- **Bulk Evaluation**: Rounds 1 and 3 use single LLM calls to evaluate all agents simultaneously for efficiency.
- **Sequential Debate**: Round 2 implements a focal-led conversation history where agents interact progressively.

### 3. Analytics & Scoring (`metrics.py`)
Handles deterministic processing of the qualitative agent outputs:
- **Numerical Mapping**: Converts semantic risk levels into comparable integers (located in `utils.py`).
- **Metric Computation**: Logic for Alignment and Fragility scores.
- **Decision Engine**: Two-stage logic that considers risk levels, shift penalties, and project context.

### 4. Data Layer & Configuration
- **Agent Registry (`agent_registry.py`)**: Centralized mapping of agent roles to their respective prompts and risk domains.
- **Shock Registry (`registry/shocks.json`)**: Configurable JSON file containing negative stress scenarios with industry and tag metadata.
- **Configuration (`config.py`)**: System-wide settings including LLM temperature, retries, and RPM rate limiting.
- **Prompts (`prompts.py`)**: Centralized semantic instructions, bulk evaluator prompts, and persona definitions.

## Data Flow
1. **Input**: User defines an initiative in the UI or JSON file.
### Simulation Sequence
1. **Round 1 (Independent Evaluation)**: All agents provide a baseline risk assessment in a single bulk LLM call.
2. **Round 2 (Focal-led Debate)**: Agents take turns as "focal leaders," initiating high-friction multi-turn discussions.
3. **Round 2 Analysis**: A structured analysis step extracts final stances, decision recommendations, and coalition mappings.
4. **Round 3 (Shock Test)**:
    - **Tag Extraction**: Deterministic keywords match the initiative to specific risk domains (e.g., `vendor`, `data`, `regulatory`).
    - **Shock Selection**: The engine filters the `shocks.json` registry for tag-relevant scenarios, falling back to industry or generic shocks as needed.
    - **Resilience Eval**: Agents provide post-shock assessments in a final bulk LLM call.
5. **Analytics**: `metrics.py` processes results into alignment and fragility scores using a **three-stage decision model**:
    - **Stage 1 (Hard Risk Gate)**: Mandatory disqualifiers.
    - **Stage 2 (Weighted Scoring)**: Metric-based decision (Proceed, Conditional, No-Go).
    - **Stage 3 (Rollout Strategy)**: Extractions of specific conditions (e.g., Pilot requirements) from debate analysis.
6. **Reporting**: LLM generates a cohesive executive assessment and action checklist.

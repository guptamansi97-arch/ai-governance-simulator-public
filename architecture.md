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
- **Risk-Agenda-Driven Debate**: Round 2 uses a two-step planning and segmented execution model. It pre-assigns unique risk topics to "owners" and manages domain-gated interjections.

### 3. Analytics & Scoring (`metrics.py`)
Handles deterministic processing of the qualitative agent outputs:
- **Numerical Mapping**: Converts semantic risk levels into comparable integers (located in `utils.py`).
- **Metric Computation**: Logic for Alignment and Fragility scores.
- **Decision Engine**: Dual-stage logic featuring:
    - `compute_baseline_decision`: Calculates initial consensus from Round 2 stances.
    - `compute_decision`: Calculates the post-stress outcome incorporating Round 3 shifts and fragility.

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
4. **Baseline Decision**: `compute_baseline_decision` generates the committee consensus based on Round 2 output.
5. **Round 3 (Shock Test)**:
    - **Tag Extraction**: Deterministic keywords match the initiative to specific risk domains (e.g., `vendor`, `data`, `regulatory`).
    - **Shock Selection**: The engine filters the `shocks.json` registry for tag-relevant scenarios, falling back to industry or generic shocks as needed.
    - **Resilience Eval**: Agents provide post-shock assessments in a final bulk LLM call.
6. **Analytics**: `metrics.py` processes results into alignment and fragility scores using a **three-stage decision model** to generate the **Post-Stress Decision**:
    - **Stage 1 (Hard Risk Gate)**: Mandatory disqualifiers (e.g., 2+ agents shifting to No-Go).
    - **Stage 2 (Weighted Scoring)**: Metric-based decision considering risk, fragility, and alignment.
    - **Stage 3 (Rollout Strategy)**: Extraction of pilot requirements and mitigations.
7. **Reporting**: LLM generates a cohesive executive assessment, comparing the baseline to the post-stress outcome, along with an action checklist.

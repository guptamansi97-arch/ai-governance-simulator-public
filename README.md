# AI Governance Stress Test Simulator

A professional strategic tool for simulating multi-agent board-level debates on AI initiatives to evaluate risk, alignment, and fragility.

## 📁 Repository Structure
This repository contains the documentation and core logic files for the simulation. 
The full implementation, including LLM agent interaction layer, prompt engineering, UI, and configuration, is maintained in a private repository.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Active Google Gemini API Key

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install google-generativeai python-dotenv streamlit pandas plotly
   ```
3. Create a `.env` file in the root and add your API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```

### Running the Simulator

#### 🖥️ Web Dashboard (Recommended)
Experience the premium executive interface:
```bash
streamlit run ui.py
```

#### 💻 CLI Mode
Run a quick simulation for the initiative defined in `data/initiative.json`:
```bash
python main.py
```

## 📖 Documentation
Detailed guides for different aspects of the system:
- [Product Overview](product.md) - What the simulator does and why.
- [System Architecture](architecture.md) - Technical design and data flow.
- [Agent Personas](agents.md) - Details on CFO, Compliance, Ops, and Evangelist roles.
- [Metrics Methodology](metrics.md) - How Alignment and Fragility are calculated.
- [Configuration Guide](config.md) - How to customize inputs and parameters.

## 🛠️ Project Structure
- `engine.py`: Central simulation orchestration engine.
- `ui.py`: Streamlit-based executive dashboard with live debate rendering and **Pilot outcome** support.
- `main.py`: CLI entry point.
- `simulation.py`: Bulk and sequential round-based reasoning logic including **Tag-based Shock Selection**.
- `registry/shocks.json`: Centralized, tag-aware repository of negative stress scenarios.
- `agent_registry.py`: Canonical registry for dynamic agent personas and domains.
- `agents.py`: LLM agent interaction layer supporting bulk calls.
- `metrics.py`: Three-stage decision logic (Hard Risk Gate + Weighted Scoring + Rollout Conditions).
- `utils.py`: Deterministic tag extraction and text cleaning helpers.
- `prompts.py`: Dynamic prompt templates for bulk and focal-led reasoning.
- `outputs/`: Directory containing all simulation logs and indices.

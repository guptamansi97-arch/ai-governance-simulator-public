import json
import os
from agents import run_bulk_agents, run_round2_analysis, run_round2_planning, run_debate_segment
from agent_registry import AGENTS
from prompts import ROUND1_INSTRUCTION, DEBATE_ROUND2_INSTRUCTION, BULK_ROUND3_INSTRUCTION
from utils import summarize_round, select_relevant_shock

# ===============================
# ROUND 1
# ===============================

def run_round1(model, initiative, on_agent_complete=None):
    """
    Round 1: Bulk baseline evaluation for all agents in registry.
    """
    context = {"initiative": initiative}
    # Dynamic: Iterates over AGENTS from registry
    results = run_bulk_agents(model, AGENTS, ROUND1_INSTRUCTION, context)
    
    # Notify progress for each agent if callback provided
    if on_agent_complete:
        for agent_name in AGENTS.keys():
            if agent_name in results:
                on_agent_complete("round1", agent_name, results[agent_name])
            
    return results


# ===============================
# ROUND 2
# ===============================


def run_round2(model, initiative, round1_results, on_agent_complete=None):
    """
    Round 2: Risk-agenda-driven debate.

    Flow:
      1. Planning call  — assigns each agent one unique risk, ranks by severity.
      2. Debate calls   — one per ranked risk; only domain-relevant agents speak.

    Returns a flat list of { speaker, message, risk_topic } dicts, fully
    compatible with perform_round2_analysis and the UI rendering layer.
    """

    conversation_history = []
    round1_summary = summarize_round(round1_results)

    # ── Step 1: Build the debate agenda ──────────────────────────────────────
    agenda_result = run_round2_planning(model, AGENTS, round1_results, initiative)
    agenda = agenda_result.get("agenda", [])

    # Fallback: if planning call returns empty, construct a minimal agenda
    # so the simulation never silently skips Round 2.
    if not agenda:
        agenda = [
            {
                "rank": i + 1,
                "severity": "Moderate",
                "risk": f"Key governance concern raised by {agent} in Round 1",
                "owner": agent,
                "flagged_by": agent,
                "eligible_interjectors": []
            }
            for i, agent in enumerate(AGENTS.keys())
        ]

    # ── Step 2: One focused debate call per agenda item ───────────────────────
    for item in agenda:
        owner        = item["owner"]
        flagged_by   = item["flagged_by"]
        interjectors = item.get("eligible_interjectors", [])
        risk_topic   = item["risk"]
        severity     = item.get("severity", "Moderate")

        # Ordered, deduplicated participant list: owner → flagged_by → interjectors
        participants = list(dict.fromkeys([owner, flagged_by] + interjectors))

        # Full persona text for every participant, injected as top-level prompt
        # blocks inside run_debate_segment (not buried in JSON).
        participant_personas = {
            name: AGENTS[name]["persona"]
            for name in participants
            if name in AGENTS
        }

        segment = {
            "risk_topic": risk_topic,
            "severity": severity,
            "owner": owner,
            "flagged_by": flagged_by,
            "eligible_interjectors": interjectors,
            "participant_personas": participant_personas
        }

        responses = run_debate_segment(
            model,
            segment,
            conversation_history,   
            round1_summary,
            initiative
        )

        if isinstance(responses, list):
            for msg in responses:
                # Tag each message with its source risk for optional UI grouping
                msg["risk_topic"] = risk_topic
                conversation_history.append(msg)
                if on_agent_complete:
                    on_agent_complete("round2", msg.get("speaker", owner), msg)

    return conversation_history

def perform_round2_analysis(model, conversation_history, round1_results=None):
    """
    Extracts structured stances and coalitions from the debate.
    """
    analysis_results = run_round2_analysis(model, conversation_history, round1_results)
    return analysis_results

# ===============================
# ROUND 3
# ===============================

def run_round3(model, initiative, round2_analysis, on_agent_complete=None):
    """
    Round 3: Bulk resilience evaluation after tag-matched shock.
    """
    # Load Registry
    registry_path = os.path.join(os.path.dirname(__file__), "registry", "shocks.json")
    with open(registry_path, "r") as f:
        shock_registry = json.load(f)
        
    # Tag-based Selection
    selected_shock_obj = select_relevant_shock(initiative, shock_registry)
    shock_text = selected_shock_obj["shock"]
    
    instruction = BULK_ROUND3_INSTRUCTION.replace("{SHOCK_SCENARIO}", shock_text)
    
    context = {
        "initiative": initiative,
        "debate_analysis": round2_analysis
    }
    
    # Dynamic: Iterates over AGENTS from registry
    results = run_bulk_agents(model, AGENTS, instruction, context)
    
    if on_agent_complete:
        for agent_name in AGENTS.keys():
            if agent_name in results:
                on_agent_complete("round3", agent_name, results[agent_name])
            
    return results, selected_shock_obj

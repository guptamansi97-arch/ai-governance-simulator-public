import json
import os
from agents import run_agent, run_bulk_agents, run_round2_analysis
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
    Round 2: Sequential debate led by each agent in registry.
    """
    conversation_history = []
    
    # Dynamic: Iterate through all agents in registry
    for focal_agent in AGENTS.keys():
        context = {
            "initiative": initiative,
            "round1_summary": summarize_round(round1_results),
            "conversation_history": conversation_history,
            "focal_agent": focal_agent
        }
        
        # Focal agent leads a multi-turn sub-session
        responses = run_agent(model, AGENTS[focal_agent]["persona"], DEBATE_ROUND2_INSTRUCTION, context)
        
        # Responses is a list of messages [ {speaker, message}, ... ]
        if isinstance(responses, list):
            for msg in responses:
                conversation_history.append(msg)
                if on_agent_complete:
                    on_agent_complete("round2", msg.get("speaker", focal_agent), msg)
                    
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
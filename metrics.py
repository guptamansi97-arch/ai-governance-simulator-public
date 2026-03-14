import statistics
from utils import risk_to_number

def compute_alignment(analysis_results):
    """
    Measures convergence after the debate using variance of risk levels
    extracted from the debate analysis.
    """
    if not analysis_results or "agent_stances" not in analysis_results:
        return 100.0

    stances = analysis_results["agent_stances"]
    risk_values = []
    
    for agent_data in stances.values():
        val = risk_to_number(agent_data.get("risk_level", "Moderate"))
        risk_values.append(val)

    if len(risk_values) < 2:
        return 100.0

    # Higher variance means lower alignment
    variance = statistics.pvariance(risk_values)
    
    # Normalize: variance of 1.0 (e.g. [2, 3]) reduces score by 40 points
    # Max variance for [1, 4] is 2.25. 100 - (2.25 * 40) = 10.
    alignment_score = max(0, 100 - (variance * 40))
    return float(round(alignment_score, 1))


def compute_fragility(round1_results, round3_results):
    """
    Calculates the fragility index (0-100) based on how much agents shifted
    their positions following the shock injection, normalized by agent count.
    """
    if not round1_results or not round3_results:
        return 0.0

    agent_count = len(round1_results)
    total_delta = 0
    penalty = 0

    for agent in round1_results.keys():
        if agent in round3_results:
            r1 = risk_to_number(round1_results[agent].get("risk_level", "Moderate"))
            r3 = risk_to_number(round3_results[agent].get("risk_level_after_shock", "Moderate"))
            
            total_delta += abs(r3 - r1)

            # Decision shift penalty
            decision_change = round3_results[agent].get("decision_change", "No Change")
            if decision_change == "Becomes No-Go":
                penalty += 30
            elif decision_change == "Becomes Conditional":
                penalty += 15

    # Normalize delta by number of agents
    avg_delta = total_delta / agent_count
    
    # Scale fragility: avg_delta of 1.0 contributes 20 points
    fragility = (avg_delta * 20) + (penalty / agent_count)
    return float(min(100, fragility))


def compute_risk_breakdown(round3_results, round1_results=None):
    """
    Maps agent post-shock evaluations to organizational risk domains.
    Uses Round 3 (post-shock) results as the primary source.
    Falls back to Round 1 baseline if an agent was not evaluated in Round 3.
    Domains are derived dynamically from agent_registry.AGENTS.
    """
    from agent_registry import AGENTS

    breakdown = {}
    for agent_name, agent_info in AGENTS.items():
        domain = agent_info.get("domain")
        if not domain:
            continue

        # Primary: Round 3 post-shock evaluation
        if round3_results and agent_name in round3_results:
            r3 = round3_results[agent_name]
            severity = r3.get("risk_level_after_shock", "Moderate")
            concerns = r3.get("primary_concerns",
                              [r3.get("vulnerability_exposed")] if r3.get("vulnerability_exposed") else [])
        # Fallback: Round 1 baseline
        elif round1_results and agent_name in round1_results:
            r1 = round1_results[agent_name]
            severity = r1.get("risk_level", "Moderate")
            concerns = r1.get("primary_concerns", [])
        else:
            continue

        breakdown[domain] = {
            "severity": severity,
            "primary_concerns": concerns if isinstance(concerns, list) else [concerns]
        }

    return breakdown


def compute_decision(round3_results, alignment_score, fragility_index, risk_appetite, round2_analysis=None):
    """
    Determines final executive decision using a three-stage calibration model.
    Stage 1: Reinforced Hard Risk Gate (requires second high risk signal or multiple shifts)
    Stage 2: Metric Score with Pilot Mitigation (-10 points for pilot consensus)
    Stage 3: Decision Mapping (Proceed < 30, Conditional 30-80, No-Go > 80)
    """
    if not round3_results:
        return {"decision": "Unknown", "conditions": []}

    conditions = []
    pilot_mitigation = 0

    # Stage 1: Reinforced Hard Risk Gate
    # Logic: Reject only if (Any Very High + At least one other High/Very High) OR (2+ shifts to No-Go)
    post_shock_risks = [agent.get("risk_level_after_shock", "Moderate") for agent in round3_results.values()]
    has_very_high = any(r == "Very High" for r in post_shock_risks)
    high_or_above_count = sum(1 for r in post_shock_risks if r in ["High", "Very High"])
    
    no_go_count = sum(1 for agent in round3_results.values() if agent.get("decision_change") == "Becomes No-Go")

    # Strict rejection condition
    if (has_very_high and high_or_above_count >= 2) or no_go_count >= 2:
        return {"decision": "Do Not Proceed", "conditions": []}

    # Stage 2: Pilot Detection & Score Mitigation
    if round2_analysis and "agent_stances" in round2_analysis:
        pilot_count = sum(1 for data in round2_analysis["agent_stances"].values() if data.get("decision") == "Pilot")
        if pilot_count >= 2:
            pilot_mitigation = -10 # Pilot acts as a risk reducer
            conditions.append("Pilot deployment required before full rollout.")

    # Stage 3: Score-Based Decision Calculation
    risks = [risk_to_number(r) for r in post_shock_risks]
    avg_risk_val = sum(risks) / len(risks)
    risk_score = (avg_risk_val - 1) / 3 * 100 

    weighted_score = (0.4 * risk_score) + (0.3 * fragility_index) + (0.3 * (100 - alignment_score))

    threshold_mod = 0
    if risk_appetite == "Low":
        threshold_mod = 10
    elif risk_appetite == "High":
        threshold_mod = -15

    # Final Score with Pilot Mitigation and Appetite modifier
    final_score = weighted_score + threshold_mod + pilot_mitigation

    # Calibrated Thresholds:
    # score < 30 → Proceed
    # 30 ≤ score ≤ 80 → Conditional Proceed
    # score > 80 → Do Not Proceed
    
    if final_score < 30:
        decision = "Proceed"
    elif final_score <= 80:
        decision = "Conditional Proceed"
    else:
        decision = "Do Not Proceed"

    # Ensure Pilot recommendations force "Conditional Proceed" if they aren't already a "Do Not Proceed"
    if "Pilot deployment required before full rollout." in conditions and decision == "Proceed":
        decision = "Conditional Proceed"

    return {
        "decision": decision,
        "conditions": conditions
    }

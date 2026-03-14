# ===============================
# INPUT SCHEMA
# ===============================

INPUT_SCHEMA = {
    "initiative_name": "string",
    "initiative_description": "string",
    "budget_range": "$0-100k | $100k-500k | $500k-1M | $1M+",
    "expected_timeline": "0-3 months | 3-6 months | 6-12 months | 12+ months",
    "industry": "Financial Services | Healthcare | Retail | SaaS | Manufacturing | Other",
    "risk_appetite": "Low | Moderate | High",
    "customer_data_involved": "boolean",
    "replaces_or_automates_human_workflow": "boolean",
    "external_vendor_or_model_provider": "boolean"
}


# ===============================
# ROUND 1 OUTPUT SCHEMA
# ===============================

ROUND1_SCHEMA = {
    "agent": "CFO | COMPLIANCE | OPERATIONS | EVANGELIST",
    "risk_level": "Low | Moderate | High",
    "confidence": "integer (0-100)",
    "primary_concerns": ["string"],
    "stance_summary": "string"
}


# ===============================
# ROUND 2 OUTPUT SCHEMA
# ===============================

ROUND2_SCHEMA = {
    "agent": "string",
    "updated_risk_level": "Low | Moderate | High",
    "confidence": "integer (0-100)",
    "position_shift": "No Change | Softened | Hardened",
    "response_to_other_concerns": ["string"],
    "revised_summary": "string"
}


# ===============================
# ROUND 3 OUTPUT SCHEMA
# ===============================

ROUND3_SCHEMA = {
    "agent": "string",
    "risk_level_after_shock": "Low | Moderate | High | Very High",
    "confidence": "integer (0-100)",
    "vulnerability_exposed": "string",
    "decision_change": "No Change | Becomes Conditional | Becomes No-Go"
}


# ===============================
# FINAL EXECUTIVE REPORT SCHEMA
# ===============================

FINAL_REPORT_SCHEMA = {
    "executive_summary": {
        "decision": "Proceed | Conditional Proceed | Do Not Proceed",
        "major_drivers_of_risk": "string",
        "overall_initiative_risk": "Very High | High | Moderate | Low",
        "risk_progression_post_stress_test": "string",
        "required_mitigations": "string",
        "bottom_line": "string"
    },
    "risk_breakdown": {
        "financial": {
            "severity": "Low | Moderate | High",
            "primary_concerns": ["string"]
        },
        "compliance": {
            "severity": "Low | Moderate | High",
            "primary_concerns": ["string"]
        },
        "operational": {
            "severity": "Low | Moderate | High",
            "primary_concerns": ["string"]
        },
        "strategic": {
            "severity": "Low | Moderate | High",
            "primary_concerns": ["string"]
        }
    },
    "action_checklist": [
        {
            "action": "string",
            "priority": "High | Medium | Low",
            "owner": "CFO | COMPLIANCE | OPERATIONS | EVANGELIST | CROSS-FUNCTIONAL"
        }
    ],
    "metrics": {
        "alignment_score": "float",
        "fragility_index": "float"
    }
}
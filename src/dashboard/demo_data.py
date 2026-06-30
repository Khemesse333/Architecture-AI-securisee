import random
from datetime import datetime, timedelta, timezone

# Référence temporelle figée pour la simulation déterministe (30 Juin 2026)
BASE_TIME = datetime(2026, 6, 30, 0, 0, 0, tzinfo=timezone.utc)

def generate_fleet(count=30):
    # Fixer la graine au début de la fonction garantit la reproductibilité à chaque appel
    random.seed(42)
    
    agent_types = ["CustomerSupportAgent", "DataAnalysisAgent", "SecurityAuditAgent", "PaymentGatewayAgent", "InvoicingAgent"]
    states = ["active", "active", "active", "provisioned", "suspended", "orphaned", "pending_approval"]
    owners = ["Finance-IT", "SecOps-Core", "Customer-Success", "Data-Science-Platform", "HR-Operations"]
    
    agents = []
    for i in range(count):
        has_id = random.random() > 0.15  # 15% de Shadow Agents
        state = random.choice(states) if has_id else "orphaned"
        risk_score = random.randint(10, 95)
        
        if risk_score > 75: risk_level = "critical"
        elif risk_score > 50: risk_level = "high"
        elif risk_score > 25: risk_level = "medium"
        else: risk_level = "low"
            
        agents.append({
            "id": f"agt-uuid-00{i}",
            "name": f"Agent-{i:02d}",
            "type": random.choice(agent_types),
            "state": state,
            "owner": random.choice(owners) if has_id else "Unknown / Unassigned",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "trust_score": random.randint(200, 990) if state == "active" else random.randint(0, 400),
            "has_identity": has_id,
            "heartbeat_count": random.randint(100, 5000),
            "credential_expires": (BASE_TIME + timedelta(days=random.randint(5, 90))).strftime("%Y-%m-%d") if state == "active" else None,
            "evidence_count": random.randint(0, 12) if not has_id else 0
        })
    return agents

def generate_policy_events(count=300):
    random.seed(42)
    actions = ["file_read", "network_egress", "database_query", "subprocess_spawn", "credential_access"]
    decisions = ["allow", "allow", "allow", "deny", "escalate"]
    tools = ["SystemTerminalTool", "DataExportTool", "CalculatorTool", "DatabaseReadTool", "AdminTool"]
    
    events = []
    for i in range(count):
        events.append({
            "timestamp": (BASE_TIME - timedelta(minutes=i*2)).strftime("%Y-%m-%d %H:%M:%S"),
            "agent_id": f"agt-uuid-00{random.randint(0, 29)}",
            "action": random.choice(actions),
            "tool": random.choice(tools),
            "decision": random.choice(decisions),
            "latency_ms": round(random.uniform(0.08, 2.45), 2),
            "rule_matched": f"sec-policy-rule-{random.randint(100, 105)}"
        })
    return events

def generate_trust_matrix(agents):
    random.seed(42)
    matrix = []
    active_agents = [a["name"] for a in agents if a["state"] == "active"]
    for src in active_agents[:10]:
        for dst in active_agents[:10]:
            if src != dst:
                matrix.append({
                    "from_agent": src,
                    "to_agent": dst,
                    "trust_score": random.randint(300, 1000)
                })
    return matrix

def generate_lifecycle_events(agents, count=150):
    random.seed(42)
    events = []
    actions = ["Activated", "Token Refreshed", "Suspended", "Deregistered", "State Polled"]
    for i in range(count):
        agent = random.choice(agents)
        events.append({
            "timestamp": (BASE_TIME - timedelta(minutes=i * 5)).strftime("%Y-%m-%d %H:%M:%S"),
            "agent_name": agent["name"],
            "event_type": random.choice(actions),
            "operator": "AGT-Mesh-Automaton",
            "status": "Success"
        })
    return events
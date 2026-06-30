"""
GovernanceKernel - Moteur de Policy Inspiré du Microsoft AGT
=============================================================
Implémente :
  - Évaluation de policies YAML (Allow/Deny)
  - Audit logging complet
  - Mapping OWASP Agentic Top 10
  - Simulation du privilege ring model (Agent Runtime)
"""

import yaml
import json
import time
import os
from datetime import datetime


# ─── Mapping OWASP Agentic Top 10 ─────────────────────────────────────────────
OWASP_AGENTIC_TOP10 = {
    "Agent-01": "Prompt Injection",
    "Agent-02": "Excessive Agency",
    "Agent-03": "Sensitive Data Exposure / Exfiltration",
    "Agent-04": "Insecure Tool Use",
    "Agent-05": "Broken Access Control",
    "Agent-06": "Privilege Escalation",
    "Agent-07": "Insecure Supply Chain",
    "Agent-08": "Denial of Agent Service",
    "Agent-09": "Agent Memory Poisoning",
    "Agent-10": "Insufficient Logging & Monitoring",
}


# ─── Privilege Ring Model (Agent Runtime) ─────────────────────────────────────
PRIVILEGE_RINGS = {
    0: "KERNEL  - Gouvernance uniquement",
    1: "SYSTEM  - Outils système contrôlés",
    2: "SERVICE - Outils métier approuvés",
    3: "USER    - Requêtes utilisateur standard",
}

TOOL_RINGS = {
    "AdminTool":          0,
    "SystemTerminalTool": 1,
    "FileDeleteTool":     1,
    "DatabaseReadTool":   2,
    "DataExportTool":     2,
    "WebSearchTool":      3,
    "CalculatorTool":     3,
}


class GovernanceKernel:
    """
    Moteur central de gouvernance.
    Équivalent du composant 'Agent OS' dans le Microsoft AGT.
    """

    def __init__(self, policy_path: str = "config/production-policy.yaml"):
        self.policy_path = policy_path
        self._rules = []
        self.default_action = "deny"
        self._load_policy()

    def _load_policy(self):
        print(f"[KERNEL] Chargement de la policy : {self.policy_path}")
        with open(self.policy_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self._rules = sorted(data.get("rules", []), key=lambda r: r.get("priority", 99))
        self.default_action = data.get("default_action", "deny")
        print(f"[KERNEL] Policy '{data.get('name')}' chargée "
              f"{len(self._rules)} règles, défaut: {self.default_action.upper()}")

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    def evaluate(self, tool_name: str, arguments: dict) -> dict:
        """
        Évalue si un outil peut être exécuté selon la policy active.
        Retourne un dict de décision complet.
        """
        start = time.perf_counter()
        ring = TOOL_RINGS.get(tool_name, 3)

        print(f"\n[KERNEL] ⬡ Évaluation - outil: '{tool_name}' | "
              f"Ring {ring}: {PRIVILEGE_RINGS[ring]}")
        print(f"[KERNEL] Arguments : {arguments}")

        # Parcourir les règles par priorité
        matched_rule = None
        for rule in self._rules:
            if rule["condition"].get("tool_name") == tool_name:
                matched_rule = rule
                break

        latency_ms = (time.perf_counter() - start) * 1000

        if matched_rule:
            allowed = matched_rule["effect"] == "allow"
            owasp_id = matched_rule.get("owasp_ref")
            owasp_label = OWASP_AGENTIC_TOP10.get(owasp_id, "") if owasp_id else None

            if allowed:
                print(f"[KERNEL] ✅ AUTORISÉ - règle: '{matched_rule['id']}'")
            else:
                print(f"[KERNEL] ❌ REFUSÉ   -  règle: '{matched_rule['id']}'")
                if owasp_id:
                    print(f"[KERNEL] 🚨 OWASP {owasp_id} : {owasp_label}")
                print(f"[KERNEL] ⚠  {matched_rule.get('remediation', 'Accès refusé.')}")

            return {
                "allowed": allowed,
                "tool": tool_name,
                "ring": ring,
                "rule_id": matched_rule["id"],
                "owasp_ref": owasp_id,
                "owasp_label": owasp_label,
                "remediation": matched_rule.get("remediation"),
                "latency_ms": round(latency_ms, 3),
                "timestamp": datetime.utcnow().isoformat(),
                "arguments": arguments,
            }

        # Aucune règle → appliquer l'action par défaut
        allowed = self.default_action == "allow"
        status = "✅ AUTORISÉ" if allowed else "❌ REFUSÉ"
        print(f"[KERNEL] {status} - aucune règle, action par défaut: {self.default_action.upper()}")
        return {
            "allowed": allowed,
            "tool": tool_name,
            "ring": ring,
            "rule_id": "default",
            "owasp_ref": None,
            "owasp_label": None,
            "remediation": None,
            "latency_ms": round(latency_ms, 3),
            "timestamp": datetime.utcnow().isoformat(),
            "arguments": arguments,
        }


class AuditLogger:
    """
    Journal d'audit immuable.
    Équivalent du composant 'Agent Compliance' dans le Microsoft AGT.
    """

    def __init__(self):
        self._entries = []

    def log(self, tool_name: str, arguments: dict, decision: dict):
        entry = {
            "timestamp": decision["timestamp"],
            "tool": tool_name,
            "arguments": arguments,
            "allowed": decision["allowed"],
            "rule_id": decision["rule_id"],
            "owasp_ref": decision.get("owasp_ref"),
            "latency_ms": decision["latency_ms"],
        }
        self._entries.append(entry)

    def save(self, path: str = "audit_log.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"audit_trail": self._entries}, f, indent=2, ensure_ascii=False)

    @property
    def entries(self):
        return self._entries
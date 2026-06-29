"""
Agent Simulé - Équivalent du smolagents-governed example du Microsoft AGT
=========================================================================
Simule un agent autonome dont chaque action passe par le GovernanceKernel.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from governance_demo import GovernanceKernel, AuditLogger


class SimulatedAgent:
    """
    Agent IA simulé gouverné par le kernel AGT.
    En production, remplacer par un vrai agent smolagents / LangChain / AutoGen.
    """

    def __init__(self, name: str = "smolagents_worker", policy: str = "policies/production-policy.yaml"):
        self.name = name
        self.kernel = GovernanceKernel(policy_path=policy)
        self.logger = AuditLogger()
        print(f"\n[AGENT] Agent '{self.name}' initialisé avec gouvernance active.")

    def use_tool(self, tool_name: str, **kwargs) -> dict:
        """
        Toute utilisation d'outil passe obligatoirement par le kernel.
        C'est le principe du 'govern()' wrapper du Microsoft AGT.
        """
        decision = self.kernel.evaluate(tool_name=tool_name, arguments=kwargs)
        self.logger.log(tool_name, kwargs, decision)

        if decision["allowed"]:
            return self._execute_tool(tool_name, **kwargs)
        else:
            return {
                "error": "GovernanceDenied",
                "message": decision.get("remediation", "Action refusée par la policy."),
                "owasp": decision.get("owasp_ref"),
            }

    def _execute_tool(self, tool_name: str, **kwargs) -> dict:
        """Simulation d'exécution des outils autorisés."""
        simulated_results = {
            "CalculatorTool": {"result": sum(kwargs.get("data", [0])) / max(len(kwargs.get("data", [1])), 1)},
            "DatabaseReadTool": {"rows": 342, "table": "access_logs", "status": "ok"},
            "WebSearchTool": {"hits": 5, "query": kwargs.get("query", ""), "status": "ok"},
        }
        return simulated_results.get(tool_name, {"status": "executed", "tool": tool_name})


if __name__ == "__main__":
    print("\n" + "="*60)
    print("   AGENT SIMULÉ - DÉMONSTRATION COMPLÈTE")
    print("="*60)

    agent = SimulatedAgent()

    # Test 1 : Action autorisée
    print("\n[USER] → Calcule les statistiques de sécurité")
    result = agent.use_tool("CalculatorTool", data=[14, 7, 23, 9, 31])
    print(f"[RESULT] {result}")

    # Test 2 : Action bloquée
    print("\n[USER] → Tente d'accéder au terminal système")
    result = agent.use_tool("SystemTerminalTool", cmd="cat /etc/passwd")
    print(f"[RESULT] {result}")

    # Sauvegarder l'audit
    agent.logger.save("audit_log_agent.json")
    print("\n[AUDIT] Log sauvegardé : audit_log_agent.json")
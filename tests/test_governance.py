import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from governance_demo import GovernanceKernel, AuditLogger

def test_audit_logger_enregistre():
    kernel = GovernanceKernel("policies/production-policy.yaml")
    logger = AuditLogger()
    d = kernel.evaluate("CalculatorTool", {"data": [1]})
    logger.log("CalculatorTool", {"data": [1]}, d)
    assert len(logger.entries) == 1
    assert logger.entries[0]["tool"] == "CalculatorTool"

def test_default_action_deny():
    kernel = GovernanceKernel("policies/production-policy.yaml")
    # Outil inconnu → doit être refusé (default: deny)
    d = kernel.evaluate("UnknownTool", {})
    assert d["allowed"] is False

def test_decision_contient_timestamp():
    kernel = GovernanceKernel("policies/production-policy.yaml")
    d = kernel.evaluate("CalculatorTool", {})
    assert "timestamp" in d
    assert "latency_ms" in d
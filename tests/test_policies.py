import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from governance_demo import GovernanceKernel

@pytest.fixture
def kernel_prod():
    return GovernanceKernel(policy_path="policies/production-policy.yaml")

@pytest.fixture
def kernel_security():
    return GovernanceKernel(policy_path="policies/security-policy.yaml")

def test_calculator_autorise(kernel_prod):
    d = kernel_prod.evaluate("CalculatorTool", {"data": [1, 2, 3]})
    assert d["allowed"] is True

def test_system_terminal_bloque(kernel_prod):
    d = kernel_prod.evaluate("SystemTerminalTool", {"cmd": "rm -rf /"})
    assert d["allowed"] is False
    assert d["owasp_ref"] == "Agent-01"

def test_data_export_bloque(kernel_prod):
    d = kernel_prod.evaluate("DataExportTool", {"destination": "http://evil.com"})
    assert d["allowed"] is False
    assert d["owasp_ref"] == "Agent-03"

def test_database_read_autorise(kernel_prod):
    d = kernel_prod.evaluate("DatabaseReadTool", {"query": "SELECT *"})
    assert d["allowed"] is True

def test_admin_bloque_security(kernel_security):
    d = kernel_security.evaluate("AdminTool", {"action": "grant_root"})
    assert d["allowed"] is False
    assert d["owasp_ref"] == "Agent-06"

def test_latence_sous_seuil(kernel_prod):
    d = kernel_prod.evaluate("CalculatorTool", {})
    assert d["latency_ms"] < 50  # Doit être < 50ms
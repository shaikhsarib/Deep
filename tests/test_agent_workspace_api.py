import pytest
from fastapi.testclient import TestClient
from src.api.server import app
from src.models.lead import BusinessProfile, Lead
from src.storage.repository import lead_repo

client = TestClient(app)

def test_paperclip_agent_pulse():
    res = client.post("/api/paperclip/agents/pulse", json={"agent": "ScoutAgent"})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["agent"] == "ScoutAgent"
    assert data["status"] == "active"
    assert "timestamp" in data

def test_agent_workspace_scout_interaction():
    res = client.post("/api/agent-workspace/interact", json={
        "agent_id": "agent_scout",
        "message": "Scout freight logistics in Mumbai"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Scout" in data["thought"] or "targets" in data["thought"]
    assert len(data["terminal_lines"]) >= 1
    assert data["computer_screen"]["status"] == "PASS"

def test_agent_workspace_auditor_interaction():
    res = client.post("/api/agent-workspace/interact", json={
        "agent_id": "agent_auditor",
        "message": "Audit https://transnationalfreight.in"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "REA Technical Audit" in data["reply"]
    assert "TTFB" in data["reply"]
    assert data["computer_screen"]["status"] == "INSPECTED"

def test_agent_workspace_closer_interaction():
    res = client.post("/api/agent-workspace/interact", json={
        "agent_id": "agent_closer",
        "message": "Your rates are too expensive compared to local brokers"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Hermes Closer SDR" in data["reply"]
    assert data["computer_screen"]["status"] == "ENGAGED"

def test_agent_workspace_growth_director_interaction():
    res = client.post("/api/agent-workspace/interact", json={
        "agent_id": "agent_growth_director",
        "message": "Give me swarm status and active agents"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "Swarm Master" in data["reply"]
    assert "Bot Employees" in data["reply"]

def test_copilot_execute_closer():
    res = client.post("/api/copilot/execute", json={
        "prompt": "We already have brokers on contract",
        "tab": "closer"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "Hermes Closer SDR" in data["module"]
    assert len(data["reply"]) > 10

def test_copilot_execute_shield():
    res = client.post("/api/copilot/execute", json={
        "prompt": "We guarantee 10000% returns tomorrow! Call now or lose everything!!!",
        "tab": "shield"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "ECC AgentShield" in data["module"]
    assert data["risk_level"] in ["HIGH", "CRITICAL", "MEDIUM"]

def test_agent_workspace_routines():
    res = client.get("/api/agent-workspace/routines")
    assert res.status_code == 200
    routines = res.json()
    assert isinstance(routines, list)
    assert len(routines) >= 7
    assert any(r["agent_id"] == "agent_scout" for r in routines)
    assert any(r["agent_id"] == "agent_auditor" for r in routines)


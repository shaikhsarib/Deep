import pytest
from fastapi.testclient import TestClient
from src.api.server import app
from src.models.lead import Lead, BusinessProfile, LeadStatus, OutreachChannel
from src.storage.repository import lead_repo
from src.services.workforce import workforce_manager

client = TestClient(app)

def test_workspace_hierarchy_contract():
    """Verifies Workspace -> Team -> Agent -> Computer hierarchy."""
    res = client.get("/api/workspace/hierarchy")
    assert res.status_code == 200
    data = res.json()
    
    # 1. Workspace
    assert "workspace" in data
    assert data["workspace"]["id"] == "deep_core_workspace"
    
    # 2. Teams
    assert "teams" in data
    assert len(data["teams"]) == 3
    team_ids = [t["id"] for t in data["teams"]]
    assert "team_revenue_intelligence" in team_ids
    assert "team_outbound_synthesis" in team_ids
    assert "team_governance_closing" in team_ids
    
    # 3. Workflows
    assert "workflows" in data
    assert len(data["workflows"]) >= 1
    assert data["workflows"][0]["id"] == "wf_autonomous_sdr"
    assert len(data["workflows"][0]["stages"]) == 10
    
    # 4. Computers (Execution Environments)
    assert "computers" in data
    assert len(data["computers"]) >= 4
    comp_agents = [c["agent_id"] for c in data["computers"]]
    assert "agent_auditor" in comp_agents
    assert "agent_scout" in comp_agents
    assert "agent_closer" in comp_agents
    assert "agent_security_shield" in comp_agents

def test_complete_connected_sdr_journey():
    """
    End-to-end verification of the 10-step connected SDR journey:
    Discovery -> Enrichment -> Technical Audit -> Evidence Grounding ->
    Outreach Synthesis -> ECC Shield -> Approvals Gate -> Delivery ->
    Reply Objection Triage -> Meeting Booking & Measurable Outcomes.
    """
    journey_id = "lead_e2e_journey_test"
    
    # Step 1: Lead Discovery (Scout creates lead)
    profile = BusinessProfile(
        company_name="Apex Global Logistics",
        business_type="freight transport logistics",
        location="Navi Mumbai",
        phone="+91 98200 99887",
        has_website=False,
        source="scout_stealth_crawler"
    )
    initial_lead = Lead(id=journey_id, profile=profile, status=LeadStatus.DISCOVERED)
    lead_repo.save(initial_lead)
    
    # Step 2-7: Process through unified workforce swarm pipeline
    staged_lead = workforce_manager.process_lead_through_pipeline(initial_lead)
    
    # Verify Step 3: Technical Audit generated
    assert staged_lead.audit is not None
    assert len(staged_lead.audit.key_flaws) > 0
    
    # Verify Step 4: Pstack proof bundle compiled
    assert staged_lead.pstack_proof is not None
    assert staged_lead.pstack_proof["verified_claims"] > 0
    
    # Verify Step 5: Grounded outreach draft created
    assert staged_lead.draft is not None
    assert staged_lead.draft.whatsapp_message is not None
    assert len(staged_lead.draft.whatsapp_message) > 20
    
    # Verify Step 6 & 7: Circuit Breaker Staging in Approvals Gate
    assert staged_lead.status == LeadStatus.PENDING_APPROVAL
    
    # Verify Step 8: Human Approval Gate Dispatch via API
    res_approve = client.post(f"/api/leads/{journey_id}/approve", json={"channel": "whatsapp", "notes": "E2E Verified"})
    assert res_approve.status_code == 200
    assert res_approve.json()["success"] is True
    
    delivered_lead = lead_repo.get_by_id(journey_id)
    assert delivered_lead.status == LeadStatus.CONTACTED
    assert OutreachChannel.WHATSAPP in delivered_lead.contacted_channels
    assert delivered_lead.last_contacted_at is not None
    
    # Verify Step 9: Inbound Reply & Objection Handling via Hermes Closer SDR
    prospect_objection = "Your rates look high, why shouldn't we continue booking through traditional brokers?"
    res_reply = client.post(f"/api/leads/{journey_id}/reply", json={"message": prospect_objection})
    assert res_reply.status_code == 200
    reply_data = res_reply.json()
    
    # Intent classified as price objection
    assert reply_data["intent"] == "price_objection"
    
    # Verify Step 10: Meeting Booking Link Insertion & Conversation Logging
    assert reply_data["booking_link_included"] is True
    assert "calendly" in reply_data["reply_message"].lower()
    
    final_lead = lead_repo.get_by_id(journey_id)
    assert len(final_lead.conversation_history) == 2
    assert final_lead.conversation_history[0]["sender"] == "prospect"
    assert final_lead.conversation_history[1]["sender"] == "closer_agent"
    
    # Clean up test lead
    lead_repo.delete(journey_id)

def test_living_agent_os_interaction_and_telemetry():
    """Verifies real execution in the Living Agent OS (3-column Rakazo environment)."""
    # 1. Scout interaction
    res_scout = client.post("/api/agent-workspace/interact", json={
        "agent_id": "agent_scout",
        "message": "Find freight carriers in Bhiwandi"
    })
    assert res_scout.status_code == 200
    assert res_scout.json()["success"] is True
    assert "terminal_lines" in res_scout.json()
    assert "computer_screen" in res_scout.json()
    
    # 2. Closer interaction
    res_closer = client.post("/api/agent-workspace/interact", json={
        "agent_id": "agent_closer",
        "message": "We already have trusted freight brokers"
    })
    assert res_closer.status_code == 200
    assert "Hermes Closer SDR" in res_closer.json()["reply"]
    
    # 3. Pulse Heartbeat
    res_pulse = client.post("/api/paperclip/agents/pulse", json={
        "agent_id": "agent_scout",
        "task": "Periodic corridor sweep"
    })
    assert res_pulse.status_code == 200
    assert res_pulse.json()["status"] == "active"


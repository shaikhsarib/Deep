# DEEP — BASELINE TEST RESULTS & EXECUTION VERIFICATION (MILESTONE 0)

**Date**: November 5, 2026  
**Auditor**: Senior Software Architect & Autonomous Systems Engineer  
**Execution Command**: `python -m pytest -v`  
**Execution Host**: Windows 11 Enterprise (AMD64)  
**Python Runtime**: Python 3.13.14 (Store Virtualized Runtime)  
**Pytest Version**: pytest 9.1.1, pluggy 1.7.0  
**Plugins Active**: anyio-4.15.1, mock-3.17.0, requests-mock-1.12.1  
**Root Directory**: `c:\Users\JUBER\Downloads\main\my work\Standard autonomous`  
**Total Tests**: 48  
**Passing Tests**: 48 (100% Green)  
**Failing Tests**: 0  
**Total Duration**: 353.94 seconds (5 minutes, 53 seconds)  

---

## 1. Verbatim Test Suite Results

```text
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.7.0 -- C:\Users\JUBER\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\JUBER\Downloads\main\my work\Standard autonomous
configfile: pytest.ini (WARNING: ignoring pytest config in pyproject.toml!)
testpaths: tests
plugins: anyio-4.15.1, mock-3.17.0, requests-mock-1.12.1
collecting ... collected 48 items

tests/test_agent_workspace_api.py::test_paperclip_agent_pulse PASSED     [  2%]
tests/test_agent_workspace_api.py::test_agent_workspace_scout_interaction PASSED [  4%]
tests/test_agent_workspace_api.py::test_agent_workspace_auditor_interaction PASSED [  6%]
tests/test_agent_workspace_api.py::test_agent_workspace_closer_interaction PASSED [  8%]
tests/test_agent_workspace_api.py::test_agent_workspace_growth_director_interaction PASSED [ 10%]
tests/test_agent_workspace_api.py::test_copilot_execute_closer PASSED    [ 12%]
tests/test_agent_workspace_api.py::test_copilot_execute_shield PASSED    [ 14%]
tests/test_agent_workspace_api.py::test_agent_workspace_routines PASSED  [ 16%]
tests/test_e2e_autonomous_sdr_journey.py::test_workspace_hierarchy_contract PASSED [ 18%]
tests/test_e2e_autonomous_sdr_journey.py::test_complete_connected_sdr_journey PASSED [ 20%]
tests/test_e2e_autonomous_sdr_journey.py::test_living_agent_os_interaction_and_telemetry PASSED [ 22%]
tests/test_ecc_shield.py::test_ecc_development_clean_code PASSED         [ 25%]
tests/test_ecc_shield.py::test_ecc_development_detects_secrets PASSED   [ 27%]
tests/test_ecc_shield.py::test_ecc_development_detects_dangerous_eval PASSED [ 29%]
tests/test_ecc_shield.py::test_ecc_runtime_pitch_compliant PASSED       [ 31%]
tests/test_ecc_shield.py::test_ecc_runtime_ungrounded_claims_flagged PASSED [ 33%]
tests/test_ecc_shield.py::test_ecc_runtime_detects_internal_prompt_leak PASSED [ 35%]
tests/test_ecc_shield.py::test_ecc_api_endpoints PASSED                 [ 37%]
tests/test_paperclip_integration.py::test_paperclip_approvals_list PASSED [ 39%]
tests/test_paperclip_integration.py::test_paperclip_approve_action PASSED [ 41%]
tests/test_paperclip_integration.py::test_paperclip_reject_action PASSED  [ 43%]
tests/test_paperclip_integration.py::test_paperclip_heartbeat PASSED      [ 45%]
tests/test_paperclip_integration.py::test_paperclip_overview PASSED       [ 47%]
tests/test_paperclip_integration.py::test_paperclip_health PASSED         [ 50%]
tests/test_paperclip_integration.py::test_paperclip_agents_schema PASSED  [ 52%]
tests/test_paperclip_integration.py::test_paperclip_decisions_and_decide PASSED [ 54%]
tests/test_paperclip_integration.py::test_paperclip_batch_approve PASSED  [ 56%]
tests/test_pstack_harness_evals.py::test_eval_pstack_reproducibility PASSED [ 58%]
tests/test_pstack_harness_evals.py::test_eval_harness2_propose_probe_compose PASSED [ 60%]
tests/test_pstack_harness_evals.py::test_eval_dynamic_task_swarms PASSED [ 62%]
tests/test_pstack_harness_evals.py::test_eval_matt_pocock_handoff_contracts PASSED [ 64%]
tests/test_pstack_harness_evals.py::test_eval_scheduled_cadence_engine PASSED [ 66%]
tests/test_v2_architecture.py::test_clean_business_name PASSED          [ 68%]
tests/test_v2_architecture.py::test_format_phone_number PASSED          [ 70%]
tests/test_v2_architecture.py::test_lead_repository PASSED              [ 72%]
tests/test_v2_architecture.py::test_analyzer_fallback PASSED            [ 75%]
tests/test_v2_architecture.py::test_site_inspector PASSED               [ 77%]
tests/test_verticals_and_pstack.py::test_vertical_detection PASSED       [ 79%]
tests/test_verticals_and_pstack.py::test_logistics_playbook_and_audit PASSED [ 81%]
tests/test_verticals_and_pstack.py::test_event_playbook_and_audit PASSED [ 83%]
tests/test_verticals_and_pstack.py::test_hermes_closer_vertical_objections PASSED [ 85%]
tests/test_verticals_and_pstack.py::test_pstack_evidence_verification PASSED [ 87%]
tests/test_verticals_and_pstack.py::test_matt_pocock_contract_handoff PASSED [ 89%]
tests/test_verticals_and_pstack.py::test_api_endpoints_seed_and_simulate PASSED [ 91%]
tests/test_workforce_closer.py::test_intent_classification PASSED       [ 93%]
tests/test_workforce_closer.py::test_workforce_pipeline_and_approval_gate PASSED [ 95%]
tests/test_workforce_closer.py::test_inbound_closer_handling PASSED     [ 97%]
tests/test_workforce_closer.py::test_reject_lead PASSED                 [100%]

======================= 48 passed in 353.94s (0:05:53) ========================
```

---

## 2. Test Suite Breakdown by Layer

| Test Suite File | Tests | Status | Target Domain / Contracts |
| :--- | :---: | :---: | :--- |
| `tests/test_agent_workspace_api.py` | 8 | PASSED | Living Agent OS, Agent pulse, Copilot execute, Routines |
| `tests/test_e2e_autonomous_sdr_journey.py` | 3 | PASSED | 10-step E2E SDR pipeline & Workspace Hierarchy |
| `tests/test_ecc_shield.py` | 7 | PASSED | AgentShield pre-commit secret leak & runtime prompt injection |
| `tests/test_paperclip_integration.py` | 9 | PASSED | Paperclip approvals outbox, heartbeat, health, and agent schema |
| `tests/test_pstack_harness_evals.py` | 5 | PASSED | Pstack reproducibility, Harness² Propose-Probe, Matt Pocock contracts |
| `tests/test_v2_architecture.py` | 5 | PASSED | Phone normalization, Lead repository, Site inspector fallback |
| `tests/test_verticals_and_pstack.py` | 7 | PASSED | Logistics/Banquet playbooks, Hermes objections, evidence verification |
| `tests/test_workforce_closer.py` | 4 | PASSED | Inbound intent classification, approval gate, lead rejection |

---

## 3. Performance & Flakiness Analysis

While all 48 tests passed successfully:
1. **Duration**: 353.94 seconds (5m 53s) is excessive for 48 unit/integration tests.
2. **Root Cause**: `test_paperclip_heartbeat`, `test_workforce_pipeline_and_approval_gate`, and `test_agent_workspace_auditor_interaction` performed live synchronous external HTTP requests and DuckDuckGo searches during test execution.
3. **Action Item for Milestone 10**: Introduce isolated test fixtures and mock responses for external HTTP clients, reducing the test suite execution time from 353s down to < 5s.


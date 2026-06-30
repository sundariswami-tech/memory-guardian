# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from google.adk.sessions.state import State, StateSchemaError
from google.adk.tools import AgentTool

from app.agent import (
    ConciergeAgent,
    HealthRecoveryAgent,
    MemoryGuardianState,
    RiskScoringAgent,
    ScreenTimeAgent,
    WebActivityAnalyzer,
    data_router,
    get_final_state,
    get_telemetry_state,
    mark_data_gathered,
    security_checkpoint,
    set_risk_metrics,
)
from app.mcp_server import (
    get_synthetic_health_metrics,
    get_synthetic_screen_time,
    get_synthetic_web_metrics,
    log_recommendation,
)


class DeterministicMockContext:
    """Mock context containing state and resume_inputs for node unit testing."""

    def __init__(self, state=None, resume_inputs=None):
        self.state = state if state is not None else {}
        self.resume_inputs = resume_inputs if resume_inputs is not None else {}


# =====================================================================
# 1. State Schema Validation
# =====================================================================


def test_memory_guardian_state_schema_properties() -> None:
    """Verify strict Pydantic typing and defaults of MemoryGuardianState."""
    state = State(value={}, delta={}, schema=MemoryGuardianState)

    # Validate defaults on the Pydantic class
    fields = MemoryGuardianState.model_fields
    assert fields["risk_score"].default == 0.0
    assert fields["web_activity_hours"].default == 0.0
    assert fields["screen_time_hours"].default == 0.0
    assert fields["sleep_hours"].default == 0.0
    assert fields["sleep_score"].default == 0.0
    assert fields["risk_level"].default == "Low"
    assert fields["approved"].default is False
    assert fields["memory_text"].default is None
    assert fields["age"].default == 0
    assert fields["data_gathered"].default is False

    # Verify that valid values work correctly
    state["risk_score"] = 99.0
    state["approved"] = True
    assert state["risk_score"] == 99.0
    assert state["approved"] is True

    # Verify that invalid type raises StateSchemaError
    with pytest.raises(StateSchemaError):
        state["risk_score"] = "invalid"


# =====================================================================
# 2. Synthetic Metric Tools
# =====================================================================


def test_get_synthetic_web_metrics() -> None:
    """Verify the output of the synthetic web activity metrics tool."""
    res = get_synthetic_web_metrics()
    assert isinstance(res, dict)
    assert "web_activity_hours" in res
    assert res["web_activity_hours"] == 2.0
    assert "active_categories" in res
    assert "social" in res["active_categories"]


def test_get_synthetic_screen_time() -> None:
    """Verify the output of the synthetic screen time metrics tool."""
    res = get_synthetic_screen_time()
    assert isinstance(res, dict)
    assert "screen_time_hours" in res
    assert res["screen_time_hours"] == 4.0
    assert "categories" in res
    assert "social" in res["categories"]


def test_get_synthetic_health_metrics() -> None:
    """Verify the output of the synthetic health metrics tool."""
    res = get_synthetic_health_metrics()
    assert isinstance(res, dict)
    assert "sleep_hours" in res
    assert res["sleep_hours"] == 5.5
    assert "sleep_score" in res
    assert res["sleep_score"] == 65.0


def test_log_recommendation() -> None:
    """Verify the response of logging a health/safety recommendation."""
    res = log_recommendation("Take a 10-minute break from screens")
    assert isinstance(res, dict)
    assert res["status"] == "logged"


# =====================================================================
# 3. Upstream Agents and ConciergeAgent Orchestration
# =====================================================================


def test_upstream_agents_configuration() -> None:
    """Verify the model, instructions, and name of downstream telemetry agents."""
    assert WebActivityAnalyzer.name == "WebActivityAnalyzer"
    assert "web activity" in WebActivityAnalyzer.instruction.lower()

    assert ScreenTimeAgent.name == "ScreenTimeAgent"
    assert "screen time" in ScreenTimeAgent.instruction.lower()

    assert HealthRecoveryAgent.name == "HealthRecoveryAgent"
    assert "health recovery" in HealthRecoveryAgent.instruction.lower()

    assert RiskScoringAgent.name == "RiskScoringAgent"
    assert "risk scoring" in RiskScoringAgent.instruction.lower()


def test_concierge_agent_orchestration_and_tool_delegation() -> None:
    """Verify that ConciergeAgent correctly delegates to the upstream agents using AgentTools."""
    assert ConciergeAgent.name == "ConciergeAgent"
    tools = ConciergeAgent.tools
    assert len(tools) == 4

    # Verify that all tools are AgentTools wrapping the telemetry agents
    agent_names = {t.agent.name for t in tools if isinstance(t, AgentTool)}
    expected_names = {
        "WebActivityAnalyzer",
        "ScreenTimeAgent",
        "HealthRecoveryAgent",
        "RiskScoringAgent",
    }
    assert agent_names == expected_names


# =====================================================================
# 4. Risk Threshold Verification
# =====================================================================


def test_risk_threshold_low() -> None:
    """Verify risk <= 50 maps to Low risk level."""
    # (100.0 - sleep_score) + (screen_time * 5.0) + (web_activity * 5.0)
    # (100 - 80) + (3 * 5) + (2 * 5) = 20 + 15 + 10 = 45.0
    mock_ctx = DeterministicMockContext(
        state={
            "web_activity_hours": 2.0,
            "screen_time_hours": 3.0,
            "sleep_score": 80.0,
        }
    )
    res = get_telemetry_state(mock_ctx)
    assert res["risk_score"] == 45.0
    assert res["risk_level"] == "Low"

    # Edge case: exactly 50
    # (100 - 80) + (3 * 5) + (3 * 5) = 20 + 15 + 15 = 50.0
    mock_ctx_50 = DeterministicMockContext(
        state={
            "web_activity_hours": 3.0,
            "screen_time_hours": 3.0,
            "sleep_score": 80.0,
        }
    )
    res_50 = get_telemetry_state(mock_ctx_50)
    assert res_50["risk_score"] == 50.0
    assert res_50["risk_level"] == "Low"


def test_risk_threshold_medium() -> None:
    """Verify risk > 50 and <= 70 maps to Medium risk level."""
    # (100.0 - sleep_score) + (screen_time * 5.0) + (web_activity * 5.0)
    # (100 - 75) + (4 * 5) + (2 * 5) = 25 + 20 + 10 = 55.0
    mock_ctx_55 = DeterministicMockContext(
        state={
            "web_activity_hours": 2.0,
            "screen_time_hours": 4.0,
            "sleep_score": 75.0,
        }
    )
    res_55 = get_telemetry_state(mock_ctx_55)
    assert res_55["risk_score"] == 55.0
    assert res_55["risk_level"] == "Medium"

    # Edge case: exactly 70.0
    # (100 - 70) + (4 * 5) + (4 * 5) = 30 + 20 + 20 = 70.0
    mock_ctx_70 = DeterministicMockContext(
        state={
            "web_activity_hours": 4.0,
            "screen_time_hours": 4.0,
            "sleep_score": 70.0,
        }
    )
    res_70 = get_telemetry_state(mock_ctx_70)
    assert res_70["risk_score"] == 70.0
    assert res_70["risk_level"] == "Medium"


def test_risk_threshold_high() -> None:
    """Verify risk > 70 maps to High risk level."""
    # (100.0 - sleep_score) + (screen_time * 5.0) + (web_activity * 5.0)
    # (100 - 60) + (4 * 5) + (3 * 5) = 40 + 20 + 15 = 75.0
    mock_ctx = DeterministicMockContext(
        state={
            "web_activity_hours": 3.0,
            "screen_time_hours": 4.0,
            "sleep_score": 60.0,
        }
    )
    res = get_telemetry_state(mock_ctx)
    assert res["risk_score"] == 75.0
    assert res["risk_level"] == "High"


def test_set_risk_metrics_tool() -> None:
    """Verify set_risk_metrics updates state correctly."""
    mock_ctx = DeterministicMockContext(state={})
    res_msg = set_risk_metrics(mock_ctx, 75.0, "High")
    assert mock_ctx.state["risk_score"] == 75.0
    assert mock_ctx.state["risk_level"] == "High"
    assert "Risk metrics set" in res_msg


# =====================================================================
# 5. Security Checkpoint and Gating Logic
# =====================================================================


def test_security_checkpoint_low_medium_risk_auto_approve() -> None:
    """Verify that security_checkpoint auto-approves and bypasses HITL for low/medium risk (<= 70)."""
    # 1. Medium Risk (65.0)
    mock_ctx = DeterministicMockContext(
        state={"risk_score": 65.0, "approved": False, "age": 30},
        resume_inputs={},
    )
    res = security_checkpoint._func(mock_ctx)
    assert res is None
    assert mock_ctx.state["approved"] is True

    # 2. Low Risk (45.0)
    mock_ctx = DeterministicMockContext(
        state={"risk_score": 45.0, "approved": False, "age": 30},
        resume_inputs={},
    )
    res = security_checkpoint._func(mock_ctx)
    assert res is None
    assert mock_ctx.state["approved"] is True


def test_security_checkpoint_high_risk_requires_hitl() -> None:
    """Verify that security_checkpoint requests exactly one HITL checkpoint for risk > 70."""
    mock_ctx = DeterministicMockContext(
        state={"risk_score": 75.0, "approved": False, "age": 30},
        resume_inputs={},
    )
    res = security_checkpoint._func(mock_ctx)

    # Asserts one HITL checkpoint request
    assert res is not None
    assert res.interrupt_id == "checkpoint_approval"

    # Resume with approval
    mock_ctx.resume_inputs = {"checkpoint_approval": True}
    res_resume = security_checkpoint._func(mock_ctx)

    # Asserts it terminates cleanly (returns None) and updates state
    assert res_resume is None
    assert mock_ctx.state["approved"] is True


# =====================================================================
# 6. Workflow Routing and Flow Simulation
# =====================================================================


def test_workflow_routing_decisions() -> None:
    """Verify that data_router routes to concierge_agent initially and memory_guard_agent after gathering data."""
    # Scenario A: data_gathered is False
    mock_ctx_initial = DeterministicMockContext(state={"data_gathered": False})
    route_initial = data_router._func(mock_ctx_initial)
    assert route_initial == "concierge_agent"

    # Scenario B: data_gathered is True
    mock_ctx_after = DeterministicMockContext(state={"data_gathered": True})
    route_after = data_router._func(mock_ctx_after)
    assert route_after == "memory_guard_agent"


def test_workflow_low_risk_no_hitl() -> None:
    """Simulate a full low-risk workflow where no HITL is requested and the workflow terminates cleanly."""
    ctx = DeterministicMockContext(
        state={
            "risk_score": 0.0,
            "web_activity_hours": 0.0,
            "screen_time_hours": 0.0,
            "sleep_hours": 0.0,
            "sleep_score": 0.0,
            "risk_level": "Low",
            "approved": False,
            "data_gathered": False,
            "age": 30,
        },
        resume_inputs={},
    )

    # Router points to ConciergeAgent to gather telemetry
    assert data_router._func(ctx) == "concierge_agent"

    # Simulate ConciergeAgent / upstream telemetry collection
    ctx.state["web_activity_hours"] = 1.0
    ctx.state["screen_time_hours"] = 2.0
    ctx.state["sleep_score"] = 90.0

    telemetry = get_telemetry_state(ctx)
    assert telemetry["risk_score"] == 25.0
    set_risk_metrics(ctx, telemetry["risk_score"], telemetry["risk_level"])

    # Security Checkpoint check
    res = security_checkpoint._func(ctx)
    assert res is None  # Auto-approved, no checkpoint
    assert ctx.state["approved"] is True

    # Mark data gathered
    mark_data_gathered._func(ctx)
    assert ctx.state["data_gathered"] is True

    # Router points to memory_guard_agent for final state
    assert data_router._func(ctx) == "memory_guard_agent"
    final = get_final_state(ctx)
    assert final["risk_score"] == 25.0
    assert final["approved"] is True


def test_workflow_high_risk_with_single_hitl() -> None:
    """Simulate high-risk workflow requiring exactly one HITL checkpoint."""
    ctx = DeterministicMockContext(
        state={
            "risk_score": 0.0,
            "web_activity_hours": 0.0,
            "screen_time_hours": 0.0,
            "sleep_hours": 0.0,
            "sleep_score": 0.0,
            "risk_level": "Low",
            "approved": False,
            "data_gathered": False,
            "age": 30,
        },
        resume_inputs={},
    )

    # Router points to ConciergeAgent
    assert data_router._func(ctx) == "concierge_agent"

    # Simulate telemetry collection triggering high risk (> 70)
    ctx.state["web_activity_hours"] = 5.0
    ctx.state["screen_time_hours"] = 6.0
    ctx.state["sleep_score"] = 50.0

    telemetry = get_telemetry_state(ctx)
    assert telemetry["risk_score"] == 100.0  # Formula caps it at 100.0
    set_risk_metrics(ctx, 100.0, "High")

    # First pass: security_checkpoint returns HITL RequestInput
    hitl_checkpoint = security_checkpoint._func(ctx)
    assert hitl_checkpoint is not None
    assert hitl_checkpoint.interrupt_id == "checkpoint_approval"

    # Second pass: resume with approval. Ensure no second checkpoint or nested approval is requested.
    ctx.resume_inputs = {"checkpoint_approval": True}
    res_resume = security_checkpoint._func(ctx)
    assert res_resume is None  # Workflow continues cleanly
    assert ctx.state["approved"] is True

    # Mark data gathered
    mark_data_gathered._func(ctx)
    assert ctx.state["data_gathered"] is True

    # Router points to memory_guard_agent, and the workflow terminates without restarting
    assert data_router._func(ctx) == "memory_guard_agent"
    final = get_final_state(ctx)
    assert final["risk_score"] == 100.0
    assert final["approved"] is True

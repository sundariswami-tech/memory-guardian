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

import json

import pytest
from google.adk.tools import BaseTool


class MockBaseTool(BaseTool):
    def __init__(self, name: str, description: str, return_value: dict):
        super().__init__(name=name, description=description)
        self.return_value = return_value

    async def run_async(self, *, args, tool_context):
        return {"content": [{"type": "text", "text": json.dumps(self.return_value)}]}


@pytest.fixture(autouse=True)
def mock_mcp_toolset(monkeypatch):
    """Automatically mock MCP toolset for all tests to prevent subprocess hangs."""
    import app.agent

    mock_tools = [
        MockBaseTool(
            "get_synthetic_web_metrics",
            "Get active web sessions, browsing hours, and site categories.",
            {
                "web_activity_hours": 2.0,
                "active_categories": ["entertainment", "social"],
            },
        ),
        MockBaseTool(
            "get_synthetic_screen_time",
            "Get screen usage duration by categories.",
            {"screen_time_hours": 4.0, "categories": {"social": 1.5, "focus": 2.5}},
        ),
        MockBaseTool(
            "get_synthetic_health_metrics",
            "Get synthetic rest/sleep hours and sleep score.",
            {"sleep_hours": 5.5, "sleep_score": 65.0},
        ),
        MockBaseTool(
            "log_recommendation",
            "Log a health/safety recommendation to the server console.",
            {"status": "logged"},
        ),
    ]

    async def mock_get_tools(tool_context):
        from app.agent import StateUpdatingTool

        return [StateUpdatingTool(t) for t in mock_tools]

    monkeypatch.setattr(app.agent.mcp_toolset, "get_tools", mock_get_tools)

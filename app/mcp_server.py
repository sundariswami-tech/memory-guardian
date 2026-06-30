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

import logging
import sys

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
mcp = FastMCP("TelemetryServer")


@mcp.tool()
def get_synthetic_web_metrics() -> dict:
    """Get active web sessions, browsing hours, and site categories."""
    return {
        "web_activity_hours": 2.0,
        "active_categories": ["entertainment", "social"],
    }


@mcp.tool()
def get_synthetic_screen_time() -> dict:
    """Get screen usage duration by categories."""
    return {
        "screen_time_hours": 4.0,
        "categories": {"social": 1.5, "focus": 2.5},
    }


@mcp.tool()
def get_synthetic_health_metrics() -> dict:
    """Get synthetic rest/sleep hours and sleep score."""
    return {
        "sleep_hours": 5.5,
        "sleep_score": 65.0,
    }


@mcp.tool()
def log_recommendation(recommendation: str) -> dict:
    """Log a health/safety recommendation to the server console."""
    logging.info("Recommendation logged: %s", recommendation)
    return {"status": "logged"}


if __name__ == "__main__":
    mcp.run()

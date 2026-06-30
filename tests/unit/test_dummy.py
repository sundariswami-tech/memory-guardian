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

from app.agent import get_final_state


class DeterministicMockContext:
    """Mock context containing state and resume_inputs for node unit testing."""

    def __init__(self, state=None, resume_inputs=None):
        self.state = state if state is not None else {}
        self.resume_inputs = resume_inputs if resume_inputs is not None else {}


def test_dummy_with_mock_context() -> None:
    """A clean dummy test using DeterministicMockContext to verify final state extraction."""
    ctx = DeterministicMockContext(
        state={
            "risk_score": 45.0,
            "risk_level": "Low",
            "approved": True,
        }
    )
    res = get_final_state(ctx)
    assert res["risk_score"] == 45.0
    assert res["approved"] is True

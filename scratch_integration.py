import logging

from dotenv import load_dotenv
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent

logging.basicConfig(level=logging.INFO)
load_dotenv()

session_service = InMemorySessionService()
session = session_service.create_session_sync(user_id="test_user", app_name="test")
runner = Runner(node=root_agent, session_service=session_service, app_name="test")

# First run: start workflow
print("--- RUN 1 ---")
message = types.Content(
    role="user",
    parts=[
        types.Part.from_text(text="Analyze my activity levels and memory protection.")
    ],
)
events = list(
    runner.run(
        new_message=message,
        user_id="test_user",
        session_id=session.id,
        run_config=RunConfig(streaming_mode=StreamingMode.SSE),
    )
)

print(f"Number of events: {len(events)}")
for idx, event in enumerate(events):
    print(f"Event {idx}: {event}")

# Find if we got RequestInput
checkpoint_requested = False
for event in events:
    if event.content and event.content.parts:
        for part in event.content.parts:
            if part.function_call and part.function_call.name == "adk_request_input":
                checkpoint_requested = True

print(f"Checkpoint requested: {checkpoint_requested}")

# Check current state in session
saved_session = session_service.get_session_sync(
    user_id="test_user", session_id=session.id, app_name="test"
)
print("Session state after Run 1:", saved_session.state)

# Second run: resume with approval
print("\n--- RUN 2 (RESUME WITH APPROVAL) ---")
resume_msg = types.Content(
    role="user",
    parts=[
        types.Part(
            function_response=types.FunctionResponse(
                name="checkpoint_approval",
                id="checkpoint_approval",
                response={"approved": True},
            )
        )
    ],
)
events2 = list(
    runner.run(
        new_message=resume_msg,
        user_id="test_user",
        session_id=session.id,
        run_config=RunConfig(streaming_mode=StreamingMode.SSE),
    )
)

print(f"Number of events in resume: {len(events2)}")
for idx, event in enumerate(events2):
    try:
        # Check if this event contains the function response for get_final_state
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_response
                    and part.function_response.name == "get_final_state"
                ):
                    print(
                        f"--- get_final_state response: {part.function_response.response} ---"
                    )
        event_str = str(event)
        print(
            f"Event {idx}: {event_str.encode('ascii', errors='replace').decode('ascii')}"
        )
    except Exception as e:
        print(f"Failed to print event {idx}: {e}")

saved_session = session_service.get_session_sync(
    user_id="test_user", session_id=session.id, app_name="test"
)
print("Session state after Run 2:", saved_session.state)

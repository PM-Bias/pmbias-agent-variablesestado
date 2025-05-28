import logging
from google.adk.agents import LlmAgent
from .prompts import TEST_AGENT_INSTRUCTION
from .tools import test_agent_tools

logger = logging.getLogger(__name__)

# Create the Test Agent
root_agent = LlmAgent(
    name="TestAgent",
    model="gemini-2.0-flash",
    instruction=TEST_AGENT_INSTRUCTION,
    tools=test_agent_tools,
)

logger.info(f"Test Agent initialized with {len(test_agent_tools)} tools")

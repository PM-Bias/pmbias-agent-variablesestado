import logging
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger(__name__)

def get_test_number(tool_context: ToolContext) -> dict:
    """
    Retrieves the test number from session state.
    This tool demonstrates accessing custom session state values.
    
    Args:
        tool_context: The tool context containing session information.
        
    Returns:
        A dictionary containing the test number or an error message.
    """
    # Debug logging to understand the state structure
    logger.info(f"=== DEBUG: State Investigation ===")
    logger.info(f"tool_context type: {type(tool_context)}")
    logger.info(f"tool_context.state type: {type(tool_context.state)}")
    
    # Try to get the state dictionary
    try:
        state_dict = tool_context.state.to_dict()
        logger.info(f"tool_context.state.to_dict(): {state_dict}")
        logger.info(f"Keys in state: {list(state_dict.keys())}")
    except Exception as e:
        logger.error(f"Error getting state dict: {e}")
    
    # Also log the session state directly
    try:
        session_state = tool_context._invocation_context.session.state
        logger.info(f"Direct session state type: {type(session_state)}")
        logger.info(f"Direct session state contents: {session_state}")
        if isinstance(session_state, dict):
            logger.info(f"Keys in direct session state: {list(session_state.keys())}")
    except Exception as e:
        logger.error(f"Error accessing direct session state: {e}")
    
    # Try multiple ways to get the test_number
    test_number = None
    
    # Method 1: tool_context.state.get()
    try:
        test_number = tool_context.state.get("test_number")
        logger.info(f"Method 1 (tool_context.state.get): {test_number}")
    except Exception as e:
        logger.error(f"Method 1 failed: {e}")
    
    # Method 2: direct session state
    if test_number is None:
        try:
            test_number = tool_context._invocation_context.session.state.get("test_number")
            logger.info(f"Method 2 (session.state.get): {test_number}")
        except Exception as e:
            logger.error(f"Method 2 failed: {e}")
    
    # Method 3: Check if it's in the state dict
    if test_number is None:
        try:
            state_dict = tool_context.state.to_dict()
            if "test_number" in state_dict:
                test_number = state_dict["test_number"]
                logger.info(f"Method 3 (from state dict): {test_number}")
        except Exception as e:
            logger.error(f"Method 3 failed: {e}")
    
    logger.info(f"=== Final test_number value: {test_number} ===")
    
    if test_number is not None:
        logger.info(f"Successfully retrieved test_number: {test_number}")
        return {
            "status": "success",
            "test_number": test_number,
            "message": f"Your exam grade is {test_number}."
        }
    else:
        logger.warning("test_number not found in session state")
        return {
            "status": "error",
            "message": "No test number found in session state. Please ensure 'test_number' was set when creating the session.",
            "debug_info": "Check the logs for detailed state information"
        }

# Create the FunctionTool instance
get_test_number_tool = FunctionTool(func=get_test_number)

# List of tools for this agent
test_agent_tools = [get_test_number_tool]

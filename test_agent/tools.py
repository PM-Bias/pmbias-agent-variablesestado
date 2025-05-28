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
    # The state is nested under another 'state' key when passed via REST API
    # This happens because the entire POST body is stored in the session state
    state_data = tool_context.state.get("state", {})
    test_number = state_data.get("test_number")
    
    if test_number is not None:
        logger.info(f"Retrieved test_number from session state: {test_number}")
        return {
            "status": "success",
            "test_number": test_number,
            "message": f"Your exam grade is {test_number}."
        }
    else:
        logger.warning("test_number not found in session state")
        return {
            "status": "error",
            "message": "No test number found in session state. Please ensure 'test_number' was set when creating the session."
        }

def get_user_name(tool_context: ToolContext) -> dict:
    """
    Retrieves the user name from userdata in session state.
    """
    # Access userdata from the top level of session state
    userdata = tool_context.state.get("userdata", {})
    user_name = userdata.get("user_name")
    
    if user_name is not None:
        logger.info(f"Retrieved user_name from userdata: {user_name}")
        return {
            "status": "success",
            "user_name": user_name,
            "message": f"The user's name is {user_name}."
        }
    else:
        logger.warning("user_name not found in userdata")
        return {
            "status": "error",
            "message": "No user name found in userdata."
        }

def create_local_lastname(lastname: str, tool_context: ToolContext) -> dict:
    """
    Creates a new lastname value in the userdata section of session state.
    
    Args:
        lastname: The lastname to create
        tool_context: The tool context containing session information.
    """
    # Get or create userdata dictionary
    userdata = tool_context.state.get("userdata", {})
    
    # Check if lastname already exists
    if "lastname" in userdata:
        return {
            "status": "error",
            "message": f"Lastname already exists with value: {userdata['lastname']}. Use update_local_lastname to change it."
        }
    
    # Create the lastname
    userdata["lastname"] = lastname
    tool_context.state["userdata"] = userdata
    
    logger.info(f"Created lastname in userdata: {lastname}")
    return {
        "status": "success",
        "message": f"Successfully created lastname: {lastname}"
    }

def update_local_lastname(new_lastname: str, tool_context: ToolContext) -> dict:
    """
    Updates an existing lastname value in the userdata section of session state.
    
    Args:
        new_lastname: The new lastname value
        tool_context: The tool context containing session information.
    """
    # Get userdata dictionary
    userdata = tool_context.state.get("userdata", {})
    
    # Check if lastname exists
    if "lastname" not in userdata:
        return {
            "status": "error",
            "message": "No lastname exists to update. Use create_local_lastname first."
        }
    
    old_lastname = userdata["lastname"]
    userdata["lastname"] = new_lastname
    tool_context.state["userdata"] = userdata
    
    logger.info(f"Updated lastname from {old_lastname} to {new_lastname}")
    return {
        "status": "success",
        "message": f"Successfully updated lastname from '{old_lastname}' to '{new_lastname}'"
    }

def read_local_lastname(tool_context: ToolContext) -> dict:
    """
    Reads the lastname value from the userdata section of session state.
    """
    # Get userdata dictionary
    userdata = tool_context.state.get("userdata", {})
    lastname = userdata.get("lastname")
    
    if lastname is not None:
        logger.info(f"Retrieved lastname from userdata: {lastname}")
        return {
            "status": "success",
            "lastname": lastname,
            "message": f"The lastname is {lastname}."
        }
    else:
        logger.warning("lastname not found in userdata")
        return {
            "status": "error",
            "message": "No lastname found in userdata. Use create_local_lastname to create one."
        }

# Create FunctionTool instances
get_test_number_tool = FunctionTool(func=get_test_number)
get_user_name_tool = FunctionTool(func=get_user_name)
create_lastname_tool = FunctionTool(func=create_local_lastname)
update_lastname_tool = FunctionTool(func=update_local_lastname)
read_lastname_tool = FunctionTool(func=read_local_lastname)

# List of tools for this agent
test_agent_tools = [
    get_test_number_tool,
    get_user_name_tool,
    create_lastname_tool,
    update_lastname_tool,
    read_lastname_tool
]

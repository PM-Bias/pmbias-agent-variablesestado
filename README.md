# Test Agent - Custom Session State Demo

This agent demonstrates how to access and modify custom session state values that are passed when creating a session.

## Features

1. **Read custom values** from different sections of session state
2. **Create new values** dynamically in session state
3. **Update existing values** in session state
4. **Manage complex nested state structures**

## How it works

1. When creating a session via the ADK API, you can pass custom state values with multiple top-level keys:
   ```json
   {
     "state": {
       "test_number": 85
     },
     "userdata": {
       "user_name": "miguel"
     }
   }
   ```

2. **Important:** The entire POST body is stored in the session state. The agent's tools access values using the appropriate nested paths:
   ```python
   # For values under "state":
   state_data = tool_context.state.get("state", {})
   test_number = state_data.get("test_number")
   
   # For values under "userdata":
   userdata = tool_context.state.get("userdata", {})
   user_name = userdata.get("user_name")
   ```

3. **Dynamic State Updates:** Tools can create and update values in the session state:
   ```python
   # Create or update a section
   userdata = tool_context.state.get("userdata", {})
   userdata["lastname"] = "New Value"
   tool_context.state["userdata"] = userdata
   ```

## Available Tools

1. **get_test_number** - Retrieves exam grade from the "state" section
2. **get_user_name** - Retrieves user name from the "userdata" section
3. **create_local_lastname** - Creates a new lastname in "userdata"
4. **update_local_lastname** - Updates an existing lastname in "userdata"
5. **read_local_lastname** - Reads the current lastname from "userdata"

## Testing the Agent Locally

### Step 1: Run the agent
```bash
# From the project directory
adk run project/test_agent
```

### Step 2: Create a session with custom state
```bash
curl -X POST http://localhost:8000/apps/test_agent/users/user_123/sessions/session_abc \
  -H "Content-Type: application/json" \
  -d '{
    "state": {
      "test_number": 95
    },
    "userdata": {
      "user_name": "miguel"
    }
  }'
```

### Step 3: Test reading values
```bash
# Ask for exam grade
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "test_agent",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What was my exam grade?"
      }]
    },
    "streaming": false
  }'

# Ask for user name
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "test_agent",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What is my name?"
      }]
    },
    "streaming": false
  }'
```

### Step 4: Inspect the session state

You can retrieve the full session details including the current state and all events:

```bash
GET http://localhost:8000/apps/test_agent/users/user_123/sessions/session_abc
```

This returns the complete session data:
```json
{
  "id": "session_abc",
  "app_name": "test_agent",
  "user_id": "user_123",
  "state": {
    "state": {
      "test_number": 95
    },
    "userdata": {
      "user_name": "miguel",
      "lastname": "Johnson"  // If created/updated by tools
    }
  },
  "events": [...],  // Full conversation history
  "last_update_time": 1748464542.46615
}
```

### Step 5: Test creating and updating values
```bash
# Create a lastname
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "test_agent",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Create a lastname Garcia for me"
      }]
    },
    "streaming": false
  }'

# Update the lastname
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "test_agent",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "Change my lastname to Rodriguez"
      }]
    },
    "streaming": false
  }'

# Read the lastname
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "test_agent",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
      "role": "user",
      "parts": [{
        "text": "What is my lastname?"
      }]
    },
    "streaming": false
  }'
```

## Key Takeaways

1. **Multiple top-level keys**: You can pass multiple sections (like "state" and "userdata") when creating a session
2. **Dynamic state management**: Agents can create and modify values in session state through tools
3. **Persistent across conversation**: Values created or updated by tools persist throughout the session
4. **Nested structure**: The entire POST body becomes the session state, so access values with the appropriate paths

## Example Session State Structure

After creating a session and using the tools, the session state might look like:
```json
{
  "state": {
    "test_number": 95
  },
  "userdata": {
    "user_name": "miguel",
    "lastname": "Rodriguez"  // Created dynamically by tool
  }
}
```

This demonstrates the full capabilities of session state management in Google ADK!

## Session Inspection and Debugging

The GET session endpoint provides comprehensive visibility into your session:

```bash
curl -X GET http://localhost:8000/apps/test_agent/users/user_123/sessions/session_abc
```

This endpoint returns:
- **Current state**: Shows all values including those created/modified by tools
- **Complete event history**: Every interaction between user and agent
- **Tool execution details**: Including function calls, responses, and state changes

### Understanding the Events Array

Each event in the response shows different aspects of the conversation:

1. **User messages**:
   ```json
   {
     "content": { "parts": [{ "text": "What's my name?" }], "role": "user" },
     "author": "user"
   }
   ```

2. **Agent function calls**:
   ```json
   {
     "content": {
       "parts": [{
         "functionCall": {
           "name": "get_user_name",
           "args": {}
         }
       }]
     },
     "author": "TestAgent"
   }
   ```

3. **Function responses with state changes**:
   ```json
   {
     "content": {
       "parts": [{
         "functionResponse": {
           "name": "create_local_lastname",
           "response": { "status": "success" }
         }
       }]
     },
     "actions": {
       "state_delta": {
         "userdata": {
           "user_name": "miguel",
           "lastname": "Smith"
         }
       }
     }
   }
   ```

The `state_delta` field shows exactly what state changes occurred during tool execution, making it easy to debug and verify that tools are working correctly.

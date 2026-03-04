# Google's Agent Development Kit Course Notes

## Pre-requirements
 - Create an account in Google Cloud https://cloud.google.com/?hl=en
 - Create a new project
 - Go to https://aistudio.google.com/apikey
 - Create an API key
 - Assign key to the project
 - Connect to a billing account
 - Rename **.env.example** to **.env**
 - Add API key to .env file
 - Create a **python venv** and activate it
 - Install all **requirements.txt**

# Basic Agent Directory Structure
```
parent_folder/
    agent_folder/         # This is your agent's package directory
        __init__.py       # Must import agent.py
        agent.py          # Must define root_agent
        .env              # Environment variables
```

# Agent Development Kit CLI Commands:
`api_server` - Starts a FastAPI server for agents,  
`conformance` - Conformance testing tools for ADK,  
`create` - Creates a new app with a prepopulated agent template,  
`deploy` - Deploys agent to hosted environments,  
`eval` - Evaluates an agent given the eval sets,  
`eval_set` - Manage Eval Sets,  
`migrate` - ADK migration commands,  
`run` - Runs an interactive CLI for a certain agent,  
`web` - Starts a FastAPI server with Web UI for agents.

# Examples

## 1. Basic Agent
#### Introduction to the simplest form of ADK agents. Learn how to create a basic agent that can respond to user queries.

### To create a simple Agent:
 - Import **Agent** from **google.adk.agents**
 - Create an object of the **Agent** passing following postional arguments
      - name=`"agent_dir_name"`
      - model=`"llm_model_name"`
      - description=`"model description"`
      - instruction=`"Engineered Instructions Prompt"`
 - In terminal run `adk web` from the parent folder that contains the agent folder

## 2. Tool Agent
#### A Tool Agent extends the basic ADK Agent by incorporating tools that allow to perform actions beyond just generating text responses.

- ## Key Components of Tools
  ### 1. Built-in Tools
  #### ADK provides several built-in tools that we can use with our agents:
   - **Google Search**: Allows our agent to search the web for information
   - **Code Execution**: Enables our agent to run code snippets
   - **Vertex AI Search**: Lets ours agent search through our own data
  #### Note: Right now, for each root agent or single agent, only one built-in tool is supported

  ### 2. Custom Function Tools
  #### We can create our own tools by defining Python functions. These custom tools extend our agent's capabilities to perform specific tasks.

  ### 3. Third-Party Tools
  #### We can integrate tools from other popular external libraries, like: `LangChain Tools, CrewAI Tools`

- ## Tool Agent Implementaion
    - ### Check the code file `/2-tool-agent/tool_agent/agent.py`. There are two sections.
        ### 1. Built-in google_search Tool
          It searches the internet for queries asked in the prompt and gives the response.
          Here are some sample questions to test.
        1. `"Search for recent news about artificial intelligence"`
        2. `"Find information about Google's Agent Development Kit"`
        3. `"What are the latest advancements in quantum computing?"`

        ### 2. Custom Function 'get_current_time' Tool
          It give the exact current time in the specified format
        1. `What's the current time??`
        2. `What's the time right now`
        3. `Give me current time in this format: YYYY:MM:DD`
        4. `Give me current time in this format: YYYY:MM:DD HH:MM:SS`
      
    

  ### Best Practices for Custom Function Tools:
    - **Parameters**: Define our function parameters using standard JSON-serializable types (string, integer, list, dictionary)
    - **No Default Values**: Default values are not currently supported in ADK
    - **Return Type**: The preferred return type is a dictionary
        - If we don't return a dictionary, ADK will wrap it into a dictionary `{"result": ...}`
        - Best format for return type: `{"status": "success", "error_message": None, "result": "..."}`
    - **Docstrings**: The function's docstring serves as the tool's description and is sent to the LLM
        - Make sure to give a clarity docstring so the LLM understands how to use the tool effectively


## 3. LiteLLM
  - #### This needs OpenRouter which is paid. So skipping it for now.

## 4. Structured Outputs in ADK
#### ADK allows you to define structured data formats for agent inputs and outputs using Pydantic models:

1. `Controlled Output Format: Using output_schema ensures the LLM produces responses in a consistent JSON structure.`
2. `Data Validation: Pydantic validates that all required fields are present and correctly formatted.`
3. `Improved Downstream Processing: Structured outputs are easier to handle in downstream applications or by other agents.`

#### Note: Use structured outputs when you need guaranteed format consistency for integration with other systems or agents.

 - ## Key Concepts: Structured Data Exchange
    Structured outputs are part of ADK's broader support for structured data exchange, which includes:

    1. **input_schema**: Define expected input format (not used in this example)
    2. **output_schema**: Define required output format (used in this example)
    3. **output_key**: Store the result in session state for use by other agents (used in this example)

- ## Email Agent Implementaion
- ### Check the code file `/4-structured-outputs/email_agent/agent.py`.
  The agent generates an email based on the pydantic model (EmailContent) and sends it as response.
  Here are some sample questions to test.
  1. `Write a professional email to my team about the upcoming project deadline that has been extended by two weeks.`
  2. `Draft an email to a client explaining that we need additional information before we can proceed with their order.`
  3. `Create an email to schedule a meeting with the marketing department to discuss the new product launch strategy.`

## 5. Sessions and State
  - ### Sessions in ADK provide a way to:

    1. **Maintain State**: Store and access user data, preferences, and other information between interactions
    2. **Track Conversation History**: Automatically record and retrieve message history
    3. **Personalize Responses**: Use stored information to create more contextual and personalized agent experiences

- ## QNA Agent Implementaion
- ### Check the code file `/5-sessions-and-state/question_answering_agent/agent.py` and `/5-sessions-and-state/basic_stateful_session.py`
  The agent answers questions based on the given iniital state preferences of the user.
  Here are some sample questions to test.
  1. `What sports do I like to play?.`
  2. `What is my profession?`
  3. `What are some of my hobbies?`

## 6. Persistent Storage in ADK
 - ### What is Persistent Storage in ADK?
     In previous examples, we used `InMemorySessionService` which stores session data only in memory - this data is lost when the application stops. For real-world applications, we'll often need our agents to remember user information and conversation history long-term. This is where persistent storage comes in.

     ADK provides the `DatabaseSessionService` that allows you to store session data in a SQL database, ensuring:

    1. **Long-term Memory**: Information persists across application restarts
    2. **Consistent User Experiences**: Users can continue conversations where they left off
    3. **Multi-user Support**: Different users' data remains separate and secure
    4. **Scalability**: Works with production databases for high-scale deployments

- ## Reminder Agent Implementaion
- ### Check the code file `/6-persistent-storage/memory_agent/agent.py`, `/6-persistent-storage/utils.py` and `/6-persistent-storage/main.py`
  The reminder agent remembers the previous conversations and does following: <br>
  - `Add new reminders` <br>
  - `View existing reminders` <br>
  - `Update reminders` <br>
  - `Delete reminders` <br>
  - `Update the user's name` <br>
- Here are some sample questions to test
  1. `Can you add a reminder for my meeting tomorrow at 10 AM?`
  2. `Remind me to call my friend on Friday evening.`
  3. `What reminders do I currently have?`
  4. `Update reminder 1 to meeting tomorrow at 1 PM`
  5. `Delete 2nd reminder`
  6. `Change my name to ASH`

## 7. Multi-Agent System
  - ### What is Multi-Agent System in ADK? 
    A Multi-Agent System is an advanced pattern in the Agent Development Kit (ADK) that allows multiple specialized agents to work together to handle complex tasks. Each agent can focus on a specific domain or functionality, and they can collaborate through delegation and communication to solve problems that would be difficult for a single agent.

  - ### Key Points to Implement Multi-Agent System
    1. There should be a `Single Root Agent` (main entry point) which manages all other `Sub Agents`
    2. The Multi-Agent System Structure should be as follows:
        ```
        parent_folder/
        ├── root_agent_folder/           # Main agent package (e.g., "manager")
        │   ├── __init__.py              # Must import agent.py
        │   ├── agent.py                 # Must define root_agent
        │   ├── .env                     # Environment variables
        │   └── sub_agents/              # Directory for all sub-agents
        │       ├── __init__.py          # Empty or imports sub-agents
        │       ├── agent_1_folder/      # Sub-agent package
        │       │   ├── __init__.py      # Must import agent.py
        │       │   └── agent.py         # Must define an agent variable
        │       ├── agent_2_folder/
        │       │   ├── __init__.py
        │       │   └── agent.py
        │       └── ...
        ```
    3. All the sub_agents are passed as a list assigned to `sub_agents` argument in the root_agent.
      Ex: `sub_agents=[sub_agent1, sub_agent2]`
    4. A `sub_agent` which uses the adk's built-in tool is always passed as a tool argument via `AgentTool` Class. (check `7-multi-agent/manager/agent.py` for code reference)
    5. Make sure to mention at the subjects agent's prompts that `If users asks anything else then to Delegate to root_agent` (This makes the agent not to stuck in a deadlock loop) 
  
  - ## Multi-Agent Manager Implementaion
    - ### Check the code files `/7-multi-agent/manager/agent.py` and `/7-multi-agent/manager/sub_agents/*`
    - ### In terminal Change Directory to `/7-multi-agent/manager` and run the command `adk web` to start the server.
    - Here are some sample questions to test
      1. `Can you tell me about the stock market today?`
      2. `Tell me something funny about programming`
      3. `What's the latest tech news?`
      4. `What time is it right now?`
      5. `Open youtube.com` (Negative Case)
  
## 8. Stateful Multi-Agent
  - ### What is Stateful Multi-Agent System in ADK? 
    A Stateful Multi-Agent System building upon the Multi-Agent pattern by incorporating persistent state management across interactions. It allows agents to not only collaborate but also maintain a long-term memory of user preferences, purchase history, and conversation logs, providing a more personalized and context-aware experience.

  - ### Key Points to Implement Stateful Multi-Agent System
    1. **Persistent State Management**: Uses `DatabaseSessionService` to store session data (state and history) in a SQL database (e.g., SQLite, MySQL).
    2. **State Tracking**: Agents can read and write to the session state (e.g., `state['interaction_history']`, `state['user_name']`).
    3. **Specialized Agent Delegation**: The Root Agent routes queries to specialized sub-agents (Policy, Sales, Support, etc.) based on user intent and state.
    4. **Context-Aware Prompting**: Use state variables (like `{user_name}`, `{purchased_courses}`) directly in agent instructions to personalize responses.
    5. **History Tracking**: Implement utility functions to append user queries and agent responses to an `interaction_history` list stored in the state.

  - ## Customer Service Multi-Agent Implementaion
    - ### Check the code files `/8-stateful-multi-agent/customer_service_agent/agent.py` and the `sub_agents` directory.
    - ### Implementation Details:
      - `main.py`: Sets up `DatabaseSessionService` and the `Runner`.
      - `utils.py`: Contains logic for updating interaction history and handling asynchronous agent calls.
      - `sales_agent`: Includes a `purchase_course` tool that dynamically updates the `purchased_courses` in the session state.
    - ### In terminal Change Directory to `/8-stateful-multi-agent` and run the command `python main.py` to start the interactive chat.
    - Here are some sample questions to test:
      1. `What's my name?` (Requires session initial state)
      2. `How much does the AI Marketing Platform course cost?` (Delegates to Sales Agent)
      3. `I want to buy the AI Marketing Platform course.` (Triggers `purchase_course` tool)
      4. `What courses have I purchased?` (Checks updated state)
      5. `Can I get a refund for my course?` (Delegates to Order Agent)


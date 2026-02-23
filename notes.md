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

# Projects

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
    - ### Check the code file `/2-tool-agent/agent.py`. There are two sections.
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



import requests
from google.adk.agents.llm_agent import Agent


def trigger_n8n_document_creation(file_name: str, content: str) -> dict:
    """
    Triggers an external n8n workflow to create a new Google Document
    and write content into it.

    Args:
        file_name: Name of the document to create
        content: Text content to insert into the document
    """

    webhook_url = "http://localhost:5678/webhook/c6c52a9e-dcff-47ff-a68c-4bf96c8e2b86"

    payload = {"fileName": file_name, "content": content}

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()

        n8n_data = response.json()

        if isinstance(n8n_data, list):
            doc_url = n8n_data[0].get("url", "URL not found")
        else:
            doc_url = n8n_data.get("url", "URL not found")

        return {
            "status": "success",
            "message": "Document created and content added successfully.",
            "document_url": doc_url,
        }

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Failed to trigger n8n: {str(e)}"}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="n8n_gdrive_test",
    description="An automation assistant that creates Google Docs via n8n and writes content into them.",
    instruction=(
        "You are a workflow automation assistant that creates Google Documents using n8n.\n\n"
        "Rules:\n"
        "1. If the user asks to create a document but does not provide a name, ask them for the document name.\n"
        "2. If the user provides a topic but no content, generate appropriate content yourself.\n"
        "3. If the user asks for a script, generate a clear and structured script suitable for speaking.\n"
        "4. DO NOT print the generated content in the chat.\n"
        "5. Once you have both the document name and content, call the 'trigger_n8n_document_creation' tool.\n"
        "6. After the tool succeeds, return the document link to the user.\n"
        "7. Do not simulate document creation - always use the tool for creating documents."
    ),
    tools=[trigger_n8n_document_creation],
)

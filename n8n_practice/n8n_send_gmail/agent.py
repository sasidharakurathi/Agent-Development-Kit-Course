import requests
from google.adk.agents.llm_agent import Agent


def trigger_n8n_email_sending(recipient: str, subject: str, content: str):
    """
    Triggers an external n8n workflow to send an email.

    Args:
        recipient: Email address of the recipient
        subject: Subject of the email
        content: HTML formatted content of the email
    """

    webhook_url = "http://localhost:5678/webhook/send-an-gmail"

    payload = {
        "toMail": recipient,
        "subject": subject,
        "message": content,
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()

        n8n_data = response.json()

        if isinstance(n8n_data, list):
            email_status = n8n_data[0].get("status", "Status not found")
        else:
            email_status = n8n_data.get("status", "Status not found")

        return {
            "status": "success",
            "message": "Email sent successfully.",
            "email_status": email_status,
        }

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Failed to trigger n8n: {str(e)}"}


from typing import Any, Dict
from google.adk.agents.loop_agent import LoopAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools.tool_context import ToolContext


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Call this function ONLY when the email Draft meets all quality requirements
    (no placeholders). It signals the end of the drafting loop.
    """
    tool_context.actions.escalate = True
    return {"message": "Drafting loop exited successfully."}


def ask_user_for_missing_details(
    question: str, tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Call this tool to escalate and ask the user for specific missing details (like their name, a specific date, recipient email, or subject).
    This pauses the agent and waits for the user's response.

    Args:
        question: The exact question to present to the user.
    """
    tool_context.actions.escalate = True
    return {"status": "paused", "message": f"Paused to ask user: {question}"}


email_generator = Agent(
    model="gemini-2.5-flash",
    name="email_generator",
    output_key="email_draft",
    tools=[ask_user_for_missing_details],
    instruction="""
    You are an AI assistant that drafts email content.
    The user will provide you with the recipient, subject, and the topic or content of the email.
    Your task is to generate the HTML formatted content of the email based on the user's input.
    
    CRITICAL RULES:
    1. NEVER use placeholders like [Your Name], [Company], [Date], etc. 
    2. If you are missing specific information needed to complete the email naturally (like the sender's name or a date), OR if you are missing the recipient or subject, DO NOT guess or use a placeholder. Instead, call the `ask_user_for_missing_details` tool to ask the user for that exact information. Wait for their response before generating the email draft.
    3. Output ONLY the HTML content, nothing else. DO NOT wrap it in markdown block quotes (```html). Do not add conversational text.
    """,
)

content_validator = Agent(
    model="gemini-2.5-flash",
    name="content_validator",
    tools=[exit_loop],
    instruction="""
    You are an AI assistant that validates email drafts.
    Your job is to check the generated HTML email content for the presence of placeholders or generic template text.
    Look for things like [Your Name], [Insert Date], <Company Name>, _signature_ etc.

    If the text contains placeholders (or if it looks like the generator is talking to the user without having used a tool):
        Provide feedback listing the placeholders found, and strictly instruct the `email_generator` to use its `ask_user_for_missing_details` tool to ask the user for this specific information. 
        DO NOT call exit_loop.

    If the text does NOT contain placeholders and looks like a complete, ready-to-send email in HTML format:
        Call the `exit_loop` tool to finish the drafting phase.
        
    CURRENT EMAIL DRAFT: {email_draft}
    """,
)

email_drafting_loop = LoopAgent(
    name="email_drafting_loop",
    sub_agents=[email_generator, content_validator],
    description="Iteratively drafts and validates HTML email content until no placeholders correspond to missing information.",
    max_iterations=10,
)

email_sender = Agent(
    model="gemini-2.5-flash",
    name="email_sender",
    tools=[trigger_n8n_email_sending],
    instruction="""
    You are the final step in the email automation pipeline.
    Your job is to take the finalized properties (recipient, subject, and final HTML content) and use the `trigger_n8n_email_sending` tool to send it.
    If you don't know the recipient or subject, ask the user before sending.
    Do not simulate sending; always use the tool. Provide the success or error message back to the user based on the tool's result.
    """,
)

root_agent = SequentialAgent(
    name="n8n_send_gmail",
    description="An automation assistant that drafts (with validation loop to avoid placeholders) and sends emails via n8n.",
    sub_agents=[email_drafting_loop, email_sender],
)

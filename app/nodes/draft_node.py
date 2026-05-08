from app.clients.ollama_client import ollama_client
from app.core.settings import settings
from app.core.schemas import AgentState, DraftResult

def draft_node(state: AgentState) -> AgentState:
    """
    Use LLM to draft customer response based on:
    Message, Intent, Priority, and Policy.
    """
    print(f"\n--- [NODE] Response Drafting ---")

    # 1. Prepare context for prompt
    customer_msg = state.customer_message
    intent = state.intent_data.intent
    priority = state.priority_data.level
    policy_content = state.policy_data.content

    # 2. Build system prompt to define AI personality
    system_prompt = (
        "You are a professional, empathetic, and efficient Virtual Banking Assistant. "
        "Your goal is to provide accurate support based ONLY on the provided policy. "
        "Format your output as a clear response to the customer."
    )

    # 3. Build detailed user prompt
    user_prompt = f"""
    CONTEXT:
    - Customer Message: "{customer_msg}"
    - Detected Intent: {intent}
    - Priority Level: {priority.upper()}
    - Official Policy: "{policy_content}"

    TASK:
    Draft a professional reply to the customer. 
    1. If the priority is HIGH, ensure the tone is urgent and reassuring.
    2. If any information is missing from the customer's request to fulfill the policy requirement, mention it.
    3. Suggest the next step (e.g., waiting for delivery, checking the app, or speaking to a human agent).

    RESPONSE STRUCTURE:
    - Draft Response: [Your message here]
    - Missing Information: [List any missing data or 'None']
    - Next Action: [The suggested next step]
    """

    # 4. Call Ollama (using generation model from settings)
    raw_response = ollama_client.generate(
        model=settings.GENERATION_MODEL,
        prompt=user_prompt,
        system_prompt=system_prompt
    )

    # 5. Save result to State
    state.draft_data = DraftResult(
        draft_response=raw_response,
        tone="empathetic" if priority == "high" else "professional"
    )

    state.trace.append("Draft response generated using LLM.")
    print(f"Result: Draft completed.")

    return state
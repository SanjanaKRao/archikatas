# Guardrails

import guardrails as gr

@gr.guard("output must be a JSON object with 'grade' and 'feedback' fields.")
def get_grading_response(prompt):
    # Call LLM API
    response = call_llm_api(prompt)
    return response

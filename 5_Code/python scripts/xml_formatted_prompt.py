# XML-Formatted Prompt for Claude 3.5 Sonnet

import openai
import xml.etree.ElementTree as ET
import json

# OpenAI API key setup (if using a Claude-compatible API)
API_KEY = "your-anthropic-api-key"

def create_xml_prompt(candidate_answer, retrieved_answers):
    """
    Generates a structured XML prompt for Claude 3.5 Sonnet using candidate responses and reference answers.
    """
    root = ET.Element("prompt")

    # Instructions section
    instructions = ET.SubElement(root, "instructions")
    instructions.text = "Grade the candidate's answer based on the reference answers. Provide a grade (0-100), feedback, and confidence score."

    # Context section
    context = ET.SubElement(root, "context")
    context.text = "You are an expert software architect evaluating short-answer responses for a certification test. Your grading should be consistent with past expert evaluations."

    # Candidate Answer section
    candidate_section = ET.SubElement(root, "candidate_answer")
    candidate_section.text = candidate_answer

    # Reference Answers section
    references = ET.SubElement(root, "reference_answers")
    for idx, ans in enumerate(retrieved_answers):
        answer_element = ET.SubElement(references, "answer")
        answer_element.set("id", str(idx+1))

        short_answer = ET.SubElement(answer_element, "short_answer")
        short_answer.text = ans['short_answer']

        grade = ET.SubElement(answer_element, "grade")
        grade.text = str(ans['grade'])

        feedback = ET.SubElement(answer_element, "expert_feedback")
        feedback.text = ans['expert_feedback']

    # Evaluation Criteria section
    criteria = ET.SubElement(root, "evaluation_criteria")

    completeness = ET.SubElement(criteria, "completeness")
    completeness.text = "30% - Does the answer fully address the question?"

    accuracy = ET.SubElement(criteria, "accuracy")
    accuracy.text = "40% - Are the statements factually correct?"

    clarity = ET.SubElement(criteria, "clarity")
    clarity.text = "30% - Is the answer well-structured and easy to understand?"

    # Task section
    task = ET.SubElement(root, "task")
    task.text = "Assign a grade (0-100). Provide detailed feedback similar to expert evaluations."

    # Output Format section
    output_format = ET.SubElement(root, "output_format")
    output_format.text = "Return a JSON response with 'grade', 'feedback', and 'confidence' fields."

    # Convert to XML string
    xml_prompt = ET.tostring(root, encoding="utf-8").decode("utf-8")

    return xml_prompt

def get_llm_response(candidate_answer, retrieved_answers):
    """
    Sends the XML-structured prompt to Claude 3.5 Sonnet and retrieves the response.
    """
    xml_prompt = create_xml_prompt(candidate_answer, retrieved_answers)

    response = openai.ChatCompletion.create(
        model="claude-3.5-sonnet",
        messages=[{"role": "user", "content": xml_prompt}],
        temperature=0.3,
        max_tokens=300
    )

    # Extract response
    ai_output = response["choices"][0]["message"]["content"]

    try:
        return json.loads(ai_output)  # Convert response to JSON
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from Claude"}

# Example Usage
candidate_answer = "Microservices improve scalability by breaking applications into smaller services."
retrieved_answers = [
    {"short_answer": "Microservices enhance scalability by distributing workloads across independent services.",
     "grade": 85,
     "expert_feedback": "Good response, but could mention fault tolerance."},
    {"short_answer": "A microservices architecture enables applications to scale dynamically by allowing each service to scale separately.",
     "grade": 90,
     "expert_feedback": "Strong answer, well explained."}
]

response = get_llm_response(candidate_answer, retrieved_answers)
print(json.dumps(response, indent=4))  # Pretty-print the JSON output

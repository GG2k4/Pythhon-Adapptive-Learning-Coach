import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os
import ast
import re
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def send_prompt_to_gemini(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def clean_code_block(response: str) -> str:
    """
    Remove code block formatting (e.g., triple backticks) from the response.
    """
    # if response.startswith("```") and response.endswith("```"):
    #     # Strip triple backticks and optional language identifier
    #     response = response.strip("```")
    #     response = response.split("\n", 1)[-1]  # Remove language identifier like "python"
    match = re.search(r'\[(.*)\]', response, re.DOTALL)
    if match:
        return match.group(1).strip()  # Return the captured group inside the brackets
    return None

    return result.strip()

def get_testcase(question: str):
    prompt = f"""Write 5 test cases for the following question in valid Python list-of-dictionaries format:

[{{'input': [...], 'expected': '...'}}, ...]

Question: {question}

Example:
Question: Reverse a string.
Gemini: [{{'input': ['hello'], 'expected': 'olleh'}}, {{'input': ['world'], 'expected': 'dlrow'}}]"""

    response = send_prompt_to_gemini(prompt)
    try:
        # Clean response of code block formatting
        cleaned_response = clean_code_block(response)
        cleaned_response_new = "[" + cleaned_response + "]"
        print(cleaned_response_new)
        # Attempt to parse the cleaned response as Python code
        #test_cases = eval(cleaned_response)  # Use eval cautiously
        test_cases = ast.literal_eval(cleaned_response_new)  # Use ast.literal_eval for safer evaluation
        if isinstance(test_cases, list):
            return test_cases
    except Exception as e:
    #     try:
    #         # If `eval` fails, try parsing as JSON
    #         test_cases = json.loads(cleaned_response)
    #         return test_cases
    #     except json.JSONDecodeError:
        return f"Failed to parse response: {response}. Error: {e}"

    return response

# Example Usage
# question = "Compare two numbers a and b, and return which is larger or if both are equal."
# test_cases = get_testcase(question)


import timeit
import ast
import subprocess
from memory_profiler import memory_usage
import google.generativeai as genai
import requests
from dotenv import load_dotenv  
import os
import json
import re

load_dotenv()

def configure_genai():
    """Configure the OpenAI Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment variables.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

model = configure_genai()
# Function to execute and evaluate Python code
def evaluate_python_code(user_code, question_prompt, test_cases, topics):
    try:
        exec(user_code, globals())  # Execute the user's code
        function_name = get_function_name(user_code)  # Extract function name from the code
        
        if not function_name:
            return {"success": False, "feedback": "No function defined in the provided code."}
        
        results = []
        for test_case in test_cases:
            input_args = test_case["input"]
            expected_output = test_case["expected"]
            try:
                result = globals()[function_name](*input_args)
                passed = result == expected_output
                results.append((input_args, expected_output, result, passed))
            except Exception as e:
                results.append((input_args, expected_output, str(e), False))
        
    except Exception as exec_error:
        return {"success": False, "feedback": f"Code execution failed: {exec_error}"}

    def time_wrapper():
        for test_case in test_cases:
            globals()[function_name](*test_case["input"])
    
    try:
        execution_time = timeit.timeit(time_wrapper, number=10)
        memory_used = max(memory_usage((time_wrapper,)))
    except Exception as perf_error:
        execution_time = "Error"
        memory_used = "Error"

    quality_feedback = check_code_quality(user_code)
    llm_feedback = get_llm_feedback(question_prompt, user_code, results, execution_time, memory_used, quality_feedback, topics)
    
    return {
        "success": True,
        "test_results": results,
        "performance": {"time": execution_time, "memory": memory_used},
        "quality_feedback": quality_feedback,
        "llm_feedback": llm_feedback,
    }

def get_function_name(code):
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return node.name
    except Exception:
        return None

def check_code_quality(code):
    try:
        process = subprocess.run(
            ["flake8", "--stdin-display-name", "user_code.py", "-"],
            input=code,
            text=True,
            capture_output=True,
        )
        return process.stdout.strip() or "No style issues detected."
    except FileNotFoundError:
        return "Static analysis tools not installed (e.g., flake8)."

def send_prompt_to_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

import json

def get_llm_feedback(question, code, test_results, time, memory, quality_feedback, topics):
    """Use OpenAI's Gemini API to generate feedback."""
    prompt = f"""
    The following Python code was submitted in response to the question: "{question}".

    Code: {code}
    
    Test Results:
    {test_results}

    Performance:
    Execution Time: {time} seconds
    Memory Usage: {memory} MB

    Code Quality Analysis:
    {quality_feedback}

    Provide feedback on:
    1. Correctness (Do test results indicate correctness? Explain failures if any).
    2. Performance (Comment on time and memory usage).
    3. Code Quality (How readable, maintainable, and robust is the code?).

    Additionally, for each of the following topics, provide a grade out of 10 and explain your grading. Return the results in the following JSON format:

    For each of the following topics, provide a grade out of 10. Return the results in the following JSON format:

    The topics are {topics}

    An example output would be:
    {{
        "grades" : "[5, 6, 3, 9, 8, 4, 2]"
    }}
    """

    try:
        response = send_prompt_to_gemini(prompt)
        response_dict = json.loads(response)
        print(f"Feedback: {quality_feedback}")

        match = re.search(r'"grades" : "(\[.*\])"', response)
        print(match)
        if match:
            grades_string = match.group(1)
            topic_scores = json.loads(grades_string)
            print("List of scores:", topic_scores)
            topic_scores_dict = {}
            ind = 0
            for topic in topics:
                topic_scores_dict[topic] = topic_scores[ind]
                ind = ind + 1
            return topic_scores_dict



        # # Extract feedback
        # feedback = response_dict.get("feedback", {})
        # print(response)

        # # Extract grades for topics
        # grades = response_dict.get("grades", [])
        # topics_scores = [grade['grade'] if grade and 'grade' in grade else None for grade in grades]

        # # Normalize the scores (e.g., scale them if necessary)
        # topics_scores = [score if score is None else score / 10 for score in topics_scores]

        # # Return the list of topic scores
        # return topics_scores

    except json.JSONDecodeError:
        return "Error: Response from the LLM could not be parsed as JSON."
    except Exception as e:
        return f"Error generating feedback from LLM: {e}"


# Example Usage
# if __name__ == "__main__":
#     model = configure_genai()
#     user_code = """
# def compare_numbers(a, b):
#     if a>b:
#         return 'a is big'
#     else:
#         if a<b:
#             return 'b is big'
#         else:
#             return 'both are equal'
# """
#     question_prompt = "Write a function that compares two numbers."
#     test_cases = [
#         {"input": [1, 2], "expected": "b is big"},
#         {"input": [1, -1], "expected": "a is big"},
#         {"input": [0, 0], "expected": "both are equal"},
#     ]
#     results = evaluate_python_code(user_code, question_prompt, test_cases, topics)
#     print(results)

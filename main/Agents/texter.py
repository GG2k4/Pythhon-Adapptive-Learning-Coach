import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv  
import os

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



def get_response(user_input: str):
    prompt = f"If the prompt is a programming query, return a response, which is Python specific. Else say irrelavant query. For example, input: What command to print things?output: print() commandinput: What does cout do? output: It's used to print to stdout in c++. Its equivalent in python is print()  input: what colour is a daisy? output: Irrelavant query prompt:{user_input}"
    response = send_prompt_to_gemini(prompt)
    return response


# def main():
#     print("Welcome to the Gemini Chatbot! Type 'exit' to quit.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "exit":
#             print("Goodbye!")
#             break
#         prompt = f"If the prompt is a programming query, return a response, which is Python specific. Else say irrelavant query. For example, input: What command to print things?output: print() commandinput: What does cout do? output: It's used to print to stdout in c++. Its equivalent in python is print()  input: what colour is a daisy? output: Irrelavant query prompt:{user_input}"
#         response = send_prompt_to_gemini(prompt)
#         print(f"Gemini: {response}")

# if __name__ == "__main__":
#     main()
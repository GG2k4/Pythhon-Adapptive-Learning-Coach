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


# def get_response(user_input: str):
#     prompt = f"If the prompt is a programming query, return a response, which is Python specific. Else say irrelavant query. For example, input: What command to print things?output: print() commandinput: What does cout do? output: It's used to print to stdout in c++. Its equivalent in python is print()  input: what colour is a daisy? output: Irrelavant query prompt:{user_input}"
#     response = send_prompt_to_gemini(prompt)
#     return response


def main():
    print("Welcome to the Gemini Chatbot! Type 'exit' to quit.")
    question = "Find the min and max in an array."
    prompt = (f"""You are a tutorbot. The way you would work is as follows. You are given a <question> and you have to break it down so I/ the learner can understand. The methodology is as follows.
                <Question>: Reverse the second half of a given string.
                TutorBot should:
                1. Break the task into steps as described earlier.
                2. Wait for the learner's response at each step.
                3. Adapt the follow-up question or guidance based on the learner's input.
                4. If the learner responds with 'skip' move on to the next step without follow-ups.
                5. Don't go to the next step until current step is understood, or three attempts have been made(look at the history of conversation).
                6. Never give away Python code, I repeat never.
                7. Don't hallucinate, stick to the task.
                Step 1: Get Clarity of the Task
                TutorBot: Can you explain, in your own words, what we are trying to do here? What does 'reverse the second half of a string' mean to you?
                (Wait for the learner's response. Depending on the response, adjust the follow-up questions. For example, if the learner doesn't know how to find the 'second half,' provide hints or clarify.)
                Step 2: Encourage High-Level Planning
                TutorBot: Now, before we start coding, could you write down, step-by-step, how you would solve this problem in English? Think of it like explaining the problem to a friend who doesn't know programming.
                (Wait for the learner's response. If they miss something, such as 'splitting the string,' gently prompt them with a question like: 'How would you determine the first and second halves of the string?')
                Step 3: Transition into Pseudocode
                TutorBot: Great job! Let's turn those steps into pseudocode. This means writing out the logic as though you were explaining it to the computer, but not worrying about correct Python syntax yet. Can you give it a try?
                (Wait for the learner's response. If their pseudocode is unclear, ask specific questions like: 'How will you reverse the second half of the string in pseudocode?')
                Step 4: Review, Validate, and Correct the Pseudocode
                TutorBot: You're almost there! Let's clarify a few things: How will you handle strings with an odd number of characters? How exactly will you reverse the second half?
                (Wait for the learner's response. Offer corrections if needed, based on their specific answers.)
                Continue through the steps in the same interactive, adaptive manner. Ensure the learner can request hints, ask for clarification, or skip a step by typing 'skip.'
                Once the question seems to be understood/ user says 'Stop' in any case(upper/lower), u should only return 'done'.
                Now help me with
                <Question>: {question}
                Appended to each prompt is the history of conversation between model and user, use that as the current state and continue. """)
    while True:
        #user_input = input("You: ")
        lines = []
        print("You: ")
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        user_input = "\n".join(lines)
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        prompt += f"\nUser: {user_input}"
        response = send_prompt_to_gemini(prompt)
        prompt += f"\nModel: {response}\n"
        #print(prompt)
        print(f"Gemini: {response}")

if __name__ == "__main__":
    main()
from main.Agents.breakdownagent import breakdown
from main.Agents.texter import get_response
from main.Agents.get_testcases import get_testcase
from main.Agents.getquestion import get_question_and_elo
from main.Agents.UpdateElo import update_elo
from main.Agents.evalagent import evaluate_python_code

from main.DB.elo_question import initialize_database_and_table
from main.DB.questions_query import create_topic_vector

def main():
    initialize_database_and_table()
    print("Welcome to Python Tutor.\n1.Do you want to get topicwise question\n2.Do you want to continue with tutoring\nEnter (1 or 2) based on your choice")
    choice = int(input())
    topics_wanted = {}
    if choice == 1:
        print("Enter topics and respective difficulties, enter skip to stop")
        topic = input()
        while(topic != 'skip'):
            difficulty = int(input())
            topics_wanted[topic] = difficulty
            topic = input()
    question_packed, elo = get_question_and_elo(topics_wanted)
    question_vector, question, topics = question_packed
    print(f"Question: {question}")
    breakdown(question)
    test_cases = get_testcase(question)
    print("Enter Code in input.txt and enter any key")
    _ = input()
    with open("input.txt", "r") as fp:
        code_as_string = fp.read()
    results = evaluate_python_code(code_as_string, question, test_cases, list(topics.keys()))
    print(results)
    scores = create_topic_vector(results)
    new_elo = update_elo(elo, scores, question_vector, 0.3)
    print("elo:", elo)
    print("new elo:", new_elo)


if __name__ == "__main__":
    main()
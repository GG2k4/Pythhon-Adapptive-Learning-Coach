from main.DB.questions_query import getQuestion
from main.DB.elo_question import get_latest_elo_entry

def get_question_and_elo(topic_weights: dict):
    if not topic_weights:
        return getQuestion(get_latest_elo_entry())
    return getQuestion(topic_weights)
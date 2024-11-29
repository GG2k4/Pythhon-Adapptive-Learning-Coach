from main.DB.questions_query import getQuestion, getQuestionByTopic
from main.DB.elo_question import get_latest_elo_entry

def get_question_and_elo(topic_weights: dict):
    if not topic_weights:
        elo = get_latest_elo_entry()
        return getQuestion(elo), elo
    return getQuestionByTopic(topic_weights), topic_weights
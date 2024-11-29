from main.DB.questions_query import getQuestion
from main.DB.elo_question import get_latest_elo_entry

def get_question_and_elo():
    return getQuestion(get_latest_elo_entry())
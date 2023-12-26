
import json
from polls.models import Question, Choice


def populate_polls_database(file_json: str, clean_database: bool = True):
    if clean_database:
        Question.objects.all().delete()
        Choice.objects.all().delete()

    with open(file_json, 'r') as file:
        data = json.load(file)

    for question_text, choices_data in data.items():
        question = Question.objects.create(question_text=question_text)

        for choice_text, votes in choices_data.items():
            Choice.objects.create(question=question, choice_text=choice_text, votes=votes)



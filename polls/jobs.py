from time import sleep
from django_rq import job
from polls.models import Question


@job
def update_question_view_count(question_id: int):
    question = Question.objects.get(id=question_id)
    question_view_count += 1
    question.save()



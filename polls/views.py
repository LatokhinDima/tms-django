from django.shortcuts import render
from django.http import HttpRequest

from .models import Question


def index(request: HttpRequest):
    question = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': question}
    return render(request, 'polls/index.html', context)


def detail(request, question_id: int):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    context = {'question': question}
    return render(request, 'polls/detail.html', context)

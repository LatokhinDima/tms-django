from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Question, Choice



def index(request):
    questions = Question.objects \
                    .filter(status=Question.Status.APPROVED) \
                    .filter(status=Question.Status.APPROVED,
                            pub_date__lte=timezone.now()) \
                    .filter() \
                    .order_by('-pub_date')[:5]
    context = {'latest_question_list': questions}
    return render(request, 'polls/index.html', context)


def detail(request, question_id: int):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    context = {'question': question}
    return render(request, 'polls/detail.html', context)

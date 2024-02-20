from django.shortcuts import render
from rest_framework import viewsets, filters
from polls.models import Question, Choice
from api.serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_view(request):
    my_param_1 = request.query_params.get('my_param_1')
    my_param_2 = request.query_params.get('my_param_2')
    data = {'status': 'ok', 'param_values': [my_param_1, my_param_2]}
    return Response(data)




class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('choices')
    serializer_class = QuestionSerializer
    filter_backends = [filters.OrderingFilter]



class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer




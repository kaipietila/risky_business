from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from core.models.nlp import Entity
from core.models.nlp import Snippet
from core.models.nlp import SnippetResults
from core.serializers import EntitySerializer
from core.serializers import SnippetSerializer


def health_check(request):
    return HttpResponse("everything ok!")


class RiskSnippet(APIView):
    def get(self, request, uuid):
        pass

    def post(self, request, uuid):
        return HttpResponse('Not Implemented')


class RiskEntity(ListCreateAPIView):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

    def create(self):
        pass

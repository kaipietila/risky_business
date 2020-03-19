from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models.nlp import Snippet
from core.models.nlp import SnippetResults
from core.serializers import SnippetSerializer


def health_check(request):
    return HttpResponse("everything ok!")


class ProcessSnippet(APIView):

    def get(self, request, uuid):
        snippet = Snippet.objects.get(code=uuid)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new snippet to be processed
        """
        serializer = SnippetSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            # process results and return some results
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class Results(APIView):

    def get(self):
        pass

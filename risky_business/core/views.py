
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models.nlp import Snippet
from core.serializers import SnippetSerializer


def health_check(request):
    return HttpResponse("everything ok!")


class ProcessSnippet(APIView):

    def get(self, request):
        snippet_code = request.data['code']
        snippet = Snippet.objects.get(code=snippet_code)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new snippet to be processed
        """
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            snippet = serializer.save()
            service = snippet.nlp_service
            service.process()
            results = snippet.results_set.last().report
            data = {
                'results': results,
            }
            return JsonResponse(data, status=status.HTTP_201_CREATED)


class Results(APIView):

    def get(self, request, uuid):
        snippet = Snippet.objects.get(code=uuid)
        results = snippet.results_set.last()
        data = {
            "is_against_aup": results.is_is_against_aup,
            "report": results.report,
            "create_time": results.create_time,
            "assessed_risk_level": results.assessed_risk_level,
        }
        return JsonResponse(data)

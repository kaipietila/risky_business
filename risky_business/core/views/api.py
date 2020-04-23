
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView

from core.models.nlp import Snippet
from core.serializers import SnippetSerializer


def health_check(request):
    return HttpResponse("everything ok!")


class ProcessSnippet(APIView):

    def get(self, request):
        uuid = request.data['code']
        try:
            snippet = Snippet.objects.get(code=uuid)
        except Snippet.DoesNotExist:
            return HttpResponseNotFound
        results = snippet.results_set.last()
        data = {
            "is_against_aup": results.is_is_against_aup,
            "report": results.report,
            "create_time": results.create_time,
        }
        return JsonResponse(data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new snippet to be processed
        """
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            snippet = serializer.save()
            service = snippet.nlp_service
            service.process()
            results = snippet.results_set.last()
            data = {
                'snippet': {
                    'snippet': snippet.text,
                    'snippet_id': snippet.code,
                    'entity_id': snippet.entity_id,
                },
                'results': {
                    'results': results.report,
                    'create_time': results.create_time,
                    'is_againt_aup': results.is_against_aup,
                }
            }
            return JsonResponse(data, status=status.HTTP_201_CREATED)

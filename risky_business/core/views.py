from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view

# Create your views here.

def health_check(request):
    return HttpResponse("everything ok!")

@api_view(['POST'])
def submit_snippet(request):
    pass

@api_view(['GET'])
def get_risk_assessment(request):
    pass

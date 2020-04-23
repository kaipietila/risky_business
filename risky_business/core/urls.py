from django.urls import path

from core.views.api import ProcessSnippet
from core.views.api import health_check

urlpatterns = [
    path('health_check', health_check),
    path('process_snippet/',
        ProcessSnippet.as_view(),
        name='snippet'),
]

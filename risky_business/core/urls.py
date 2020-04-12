from django.urls import path

from core import views

urlpatterns = [
    path('', views.health_check),
    path('process_snippet/',
        views.ProcessSnippet.as_view(),
        name='snippet'),
    path('process_snippet/<uuid:uuid>/results',
        views.Results.as_view(),
        name='snippet'),
]
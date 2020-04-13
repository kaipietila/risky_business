from django.urls import path

from core import views

urlpatterns = [
    path('health_check', views.health_check),
    path('process_snippet/',
        views.ProcessSnippet.as_view(),
        name='snippet'),
]

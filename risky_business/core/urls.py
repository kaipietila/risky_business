from django.urls import path

from . import views

urlpatterns = [
    path('', views.health_check),
    path('risk_entity/', views.RiskEntity.as_view(), name='entity'),
    path('risk_snippet/<uuid:uuid>/', views.RiskSnippet.as_view(),name='snippet'),
]
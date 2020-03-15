from django.urls import path

from . import views

urlpatterns = [
    path('', views.health_check),
    path('submit_snippet/', views.submit_snippet, name='submit_snippet'),
    path('get_risk_assessment/', views.get_risk_assessment,name='get_risk'),
]
from django.urls import path
from . import views
from .predictor import detect_disease

urlpatterns = [
    path('', views.diagnose_view, name='diagnose'),
    path('api/detect/', detect_disease, name='detect_disease'),
]

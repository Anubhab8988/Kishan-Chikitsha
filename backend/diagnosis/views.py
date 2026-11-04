from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .predictor import detect_disease # Import from predictor.py
import os
from django.core.files.storage import default_storage

def diagnose_view(request):
     return render(request, 'diagnose.html')

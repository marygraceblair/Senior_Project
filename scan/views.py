from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import redirect 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import practice
import json

def simple_upload(request):
    if request.method == 'POST':
        image = request.FILES['myfile']
        practice.scan_receipt(image)
    return render(request, '../templates/import.html')

# Create your views here.

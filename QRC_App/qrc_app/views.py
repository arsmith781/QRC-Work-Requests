from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'qrc_app/index.html')

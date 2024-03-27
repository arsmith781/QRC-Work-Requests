from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic


def index(request):
    return render(request, 'qrc_app/index.html')


def forgotPassword(request):
    return render(request, 'qrc_app/forgot_password.html')


class WorkRequestListView(generic.ListView):
    model = WorkRequest


class WorkRequestDetailView(generic.DetailView):
    model = WorkRequest
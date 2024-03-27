from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic


def index(request):
    return render(request, 'qrc_app/index.html')


def forgotPassword(request):
    return render(request, 'qrc_app/forgot_password.html')


def deleteWorkRequests(request):
    if request.method == 'POST':
        id_list = request.POST.getlist('boxes')
        id_list = map(int, id_list)

        requestToDelete = []
        for id in id_list:
            requestToDelete.append(WorkRequest.objects.get(pk=id))

        print(requestToDelete)
        # delete code later

        workrequest_list = WorkRequest.objects.all()

        context = {"workrequest_list": workrequest_list}

        return render(request, 'qrc_app/workrequest_list.html', context)

    else:
        return render(request, 'qrc_app/index.html')


class WorkRequestListView(generic.ListView):
    model = WorkRequest


class WorkRequestDetailView(generic.DetailView):
    model = WorkRequest
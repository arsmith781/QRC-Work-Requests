import os

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

        for id in id_list:
            instance = WorkRequest.objects.get(id=id)
            print(instance)
            images = WorkRequestImage.objects.filter(request=instance)
            print(images)

            for image in images:
                print(image.photo.path)
                os.remove(image.photo.path)
            # get the path to the photo and delte it

            instance.delete()

        workrequest_list = WorkRequest.objects.all()

        context = {"workrequest_list": workrequest_list}

        return render(request, 'qrc_app/workrequest_list.html', context)

    else:
        return render(request, 'qrc_app/index.html')


class WorkRequestListView(generic.ListView):
    model = WorkRequest


class WorkRequestDetailView(generic.DetailView):
    model = WorkRequest
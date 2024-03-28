import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import *
from django.forms import modelformset_factory  # this is so we can have 2 forms on one page


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
            images = WorkRequestImage.objects.filter(request=instance)

            # get the path to the photo and delete it
            for image in images:
                os.remove(image.photo.path)
            instance.delete()

        workrequest_list = WorkRequest.objects.all()

        context = {"workrequest_list": workrequest_list}

        return render(request, 'qrc_app/workrequest_list.html', context)

    else:
        return render(request, 'qrc_app/index.html')


def createWorkRequests(request):
    # we need to have two forms in one since we want the user to be able to add images we well. 3 by default
    ImageFormSet = modelformset_factory(WorkRequestImage, form=ImageForm, extra=3)
    if request.method == 'POST':
        form = WorkRequestForm(request.POST)  # get the request info for the work request
        formset = ImageFormSet(request.POST, request.FILES, queryset=WorkRequestImage.objects.none())  # get the request info for the images

        if form.is_valid() and formset.is_valid():  # need to check 2 forms now
            # save work request (dont save so we can calculate the task numher
            request = form.save(commit=False)
            request.task_number = max([request.task_number for request in WorkRequest.objects.all()]) + 1
            request.save()

            # go through the images in the imageform
            for form in formset.cleaned_data:
                if form:
                    image = form['photo']
                    # create new image model with the new data
                    photo = WorkRequestImage(request=request, photo=image)
                    photo.save()

            # return to project list
            return redirect('workrequests')
    else:
        form = WorkRequestForm()
        formset = ImageFormSet(queryset=WorkRequestImage.objects.none())

    allRequests = WorkRequest.objects.all()
    taskNumbers = [request.task_number for request in allRequests]
    nextTaskNumber = max(taskNumbers) + 1  # autoincrement task number by 1

    context = {'form': form, 'formset': formset, 'nextTaskNumber': nextTaskNumber}
    return render(request, 'qrc_app/workrequests_form.html', context)


def updateWorkRequests(request, request_id):
    pass


class WorkRequestListView(generic.ListView):
    model = WorkRequest


class WorkRequestDetailView(generic.DetailView):
    model = WorkRequest
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

            # return to request list
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
    workRequest = WorkRequest.objects.get(pk=request_id)
    # this time we can delete (since we're editing)
    ImageFormSet = modelformset_factory(WorkRequestImage, form=ImageForm, extra=1, can_delete=True)
    if request.method == 'POST':
        # set the variables with form data
        # intance creates a new form instead of a new one (without it, we get a copy)
        form = WorkRequestForm(request.POST, instance=workRequest)
        formset = ImageFormSet(request.POST, request.FILES, queryset=WorkRequestImage.objects.filter(request=workRequest))  # get the request info for the images

        if form.is_valid() and formset.is_valid():  # need to check 2 forms now
            # save work request. Need task number since it's not in the form
            workRequestForm = form.save(commit=False)
            workRequestForm.task_number = workRequest.task_number
            workRequestForm.save()

            photos = formset.save(commit=False)

            # now we need to "connect" the forms by setting the new photos to be attached to the desired request
            for photo in photos:
                photo.request = workRequest
                photo.save()

            # if photo were deleted we gotta handle that both in the database AND the file system
            # similar to deleteRequest but instead of the CASCADE handling deletion we are
            for image in formset.deleted_objects:
                os.remove(image.photo.path)
                image.delete()

            # return to detail of one being views
            return redirect('workrequest-detail', pk=request_id)
    else:
        # upon get set the forms to the current request and the images in that request
        form = WorkRequestForm(instance=workRequest)
        formset = ImageFormSet(queryset=WorkRequestImage.objects.filter(request=workRequest))
    context = {'form': form, 'formset': formset, 'nextTaskNumber': workRequest.task_number}
    return render(request, 'qrc_app/workrequests_form.html', context)


class WorkRequestListView(generic.ListView):
    model = WorkRequest


class WorkRequestDetailView(generic.DetailView):
    model = WorkRequest
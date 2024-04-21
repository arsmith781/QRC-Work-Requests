import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views import generic
from .forms import *
from django.forms import modelformset_factory  # this is so we can have 2 forms on one page
from django.utils import timezone

# user auth stuff
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from.decorators import allowed_users

# email stuff
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request, 'qrc_app/index.html')


def forgotPassword(request):
    return render(request, 'qrc_app/forgot_password.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff_role'])
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

        return redirect('workrequests')

    else:
        return render(request, 'qrc_app/index.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff_role'])
def createWorkRequests(request):
    # we need to have two forms in one since we want the user to be able to add images we well. 3 uploads by default
    ImageFormSet = modelformset_factory(WorkRequestImage, form=ImageForm, extra=3)
    if request.method == 'POST':
        form = WorkRequestForm(request.POST)  # get the request info for the work request
        formset = ImageFormSet(request.POST, request.FILES, queryset=WorkRequestImage.objects.none())  # get the request info for the images

        if form.is_valid() and formset.is_valid():  # need to check 2 forms now
            # save work request (dont save so we can calculate the task numher
            workRequest = form.save(commit=False)
            workRequest.task_number = max([currentRequest.task_number for currentRequest in WorkRequest.objects.all()]) + 1 if len(WorkRequest.objects.all()) > 0 else 0
            workRequest.save()

            # go through the images in the imageform
            for form in formset.cleaned_data:
                if form:
                    image = form['photo']
                    # create new image model with the new data
                    photo = WorkRequestImage(request=workRequest, photo=image)
                    photo.save()

            # return to request list
            return redirect('workrequests')
    else:
        form = WorkRequestForm()
        formset = ImageFormSet(queryset=WorkRequestImage.objects.none())

    # autoincrement task number by 1
    allRequests = WorkRequest.objects.all()
    taskNumbers = [request.task_number for request in allRequests]
    taskNumbers = [0] if len(taskNumbers) == 0 else taskNumbers
    nextTaskNumber = max(taskNumbers) + 1

    context = {'form': form, 'formset': formset, 'nextTaskNumber': nextTaskNumber}
    return render(request, 'qrc_app/workrequests_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff_role'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Staff_role'])
def closeWorkRequest(request, request_id):
    workRequest = WorkRequest.objects.get(pk=request_id)
    ImageFormSet = modelformset_factory(WorkRequestImage, form=ImageForm, extra=1)
    if request.method == 'POST':
        print("posted")
        form = WorkRequestCloseForm(request.POST, instance=workRequest)
        formset = ImageFormSet(request.POST, request.FILES, queryset=WorkRequestImage.objects.filter(request=workRequest))  # get the request info for the images
        if form.is_valid() and formset.is_valid():  # need to check 2 forms now
            print("valid")
            workRequestForm = form.save(commit=False)

            # set the variables we didn't pass in the form
            workRequestForm.task_number = workRequest.task_number
            workRequestForm.submitter_name = workRequest.submitter_name
            workRequestForm.contact_info = workRequest.contact_info
            workRequestForm.date = workRequest.date
            workRequestForm.location = workRequest.location
            workRequestForm.description = workRequest.description
            workRequestForm.type_of_issue = workRequest.type_of_issue
            workRequestForm.assigned_worker = workRequest.assigned_worker
            workRequestForm.is_closed = True
            workRequestForm.close_date = timezone.now()  # set the time to the current time with the timezone in the settings
            workRequestForm.save()

            photos = formset.save(commit=False)

            # now we need to "connect" the forms by setting the new photos to be attached to the desired request
            for photo in photos:
                photo.request = workRequest
                photo.save()

            # return to the list
            return redirect('workrequests')
    else:
        # send some stuff to the form
        # upon get set the forms to the current request and the images in that request
        form = WorkRequestCloseForm(instance=workRequest)
        formset = ImageFormSet(queryset=WorkRequestImage.objects.filter(request=workRequest))

    context = {'form': form, 'formset': formset, 'nextTaskNumber': workRequest.task_number}
    return render(request, 'qrc_app/workrequests_form.html', context)


# user auth stuff
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # get user information

            # get some data about the user
            username = form.cleaned_data.get('username')
            firstName = form.cleaned_data.get('first_name')
            lastName = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            rentalGroup = form.cleaned_data.get('rental_group')

            # set the variables in the model
            # split into 2 ifs that do the same-ish thing for easy maintenance
            if rentalGroup:
                group = Group.objects.get(name='Rental_Group_role')
                user.groups.add(group)

                newUser = RentalGroupAccount.objects.create(user=user, )
                newUser.name = f'{firstName.capitalize()} {lastName.capitalize()}'
                newUser.contact_info = email
                newUser.is_staff = False
                newUser.is_rental_group = True
            else:
                group = Group.objects.get(name='Staff_role')
                user.groups.add(group)

                newUser = StaffAccount.objects.create(user=user, )
                newUser.name = f'{firstName.capitalize()} {lastName.capitalize()}'
                newUser.contact_info = email
                newUser.is_staff = True
                newUser.is_rental_group = False

            newUser.is_admin = False  # admin should always be false since the "real" implemention will only let staff make accounts
            newUser.save()

            # display  a message and send to login page
            messages.success(request, f'Account was created for {username}')
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


# email stuff
def sendEmail(request):
    testMessage = 'Test Message'
    testReceiveEmail = 'arsmith781@gmail.com'
    testSubject = 'Test Subject'

    returnVar = send_mail(from_email=settings.EMAIL_HOST_USER, subject=testSubject, message=testMessage, recipient_list=[testReceiveEmail], fail_silently=False)
    if returnVar == 1:  # this means an 1 email was sent:
        messages.success(request, f'Email was sent.')
    else:  # this means NO emails were sent
        messages.error(request, f'Email failed to send.')

    return render(request, 'qrc_app/index.html')


class WorkRequestListView(LoginRequiredMixin, generic.ListView):
    model = WorkRequest


class WorkRequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = WorkRequest
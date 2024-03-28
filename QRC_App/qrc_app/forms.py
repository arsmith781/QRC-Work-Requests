from django.forms import ModelForm
from .models import *


class WorkRequestForm(ModelForm):
    class Meta:
        model = WorkRequest
        fields = ('submitter_name', 'contact_info', 'location', 'sub_location', 'type_of_issue', 'description', 'assigned_worker', 'is_closed')


class ImageForm(ModelForm):
    class Meta:
        model = WorkRequestImage
        fields = ('photo',)
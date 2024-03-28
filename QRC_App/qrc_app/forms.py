from django.forms import ModelForm, Select
from .models import *



class WorkRequestForm(ModelForm):
    class Meta:
        model = WorkRequest
        fields = ('submitter_name', 'contact_info', 'location', 'sub_location', 'type_of_issue', 'description', 'assigned_worker', 'is_closed')

    def __init__(self, *args, **kwargs):
        super(WorkRequestForm, self).__init__(*args, **kwargs)

        location_value = self.instance.location if self.instance else None

        if location_value:
            self.fields['sub_location'].widget = Select(choices=WorkRequest.ROOMS[location_value])

class ImageForm(ModelForm):
    class Meta:
        model = WorkRequestImage
        fields = ('photo',)
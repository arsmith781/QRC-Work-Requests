from django.forms import ModelForm, Select
from .models import *


class WorkRequestForm(ModelForm):
    class Meta:
        model = WorkRequest
        fields = ('submitter_name', 'contact_info', 'location', 'sub_location', 'type_of_issue', 'description', 'assigned_worker', 'is_closed')

    # uncomment this code if you want to update the forms sublocation choices when it is created
    # doesn't really work if you change the location in the same form (sub location doesn't auto update)
    # try this video: https://www.youtube.com/watch?v=uU1uLYaNr9U
    # this says you need a new libray but if it work it works.
    def __init__(self, *args, **kwargs):
        super(WorkRequestForm, self).__init__(*args, **kwargs)

        location_value = self.instance.location if self.instance else None

        if location_value:
            self.fields['sub_location'].widget = Select(choices=WorkRequest.ROOMS[location_value])

    def change_sublocation(self):
        pass


class ImageForm(ModelForm):
    class Meta:
        model = WorkRequestImage
        fields = ('photo',)


class WorkRequestCloseForm(ModelForm):
    class Meta:
        model = WorkRequest
        fields = ('close_note', 'assigned_worker')

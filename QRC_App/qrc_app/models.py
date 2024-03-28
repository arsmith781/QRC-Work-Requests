from django.db import models
from django.urls import reverse


# Create your models here.
class WorkRequest(models.Model):
    task_number = models.IntegerField()
    submitter_name = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    # First value is how to store option in the databse
    # Second value is human readable string

    BUILDINGS = (
        ('Clark', 'Clark'),
        ('Turner', 'Turner'),
        ('Fell', 'Fell'),
        ('Chapel', 'Chapel'),
        ('Kinser', 'Kinser'),
        ('Big Bear', 'Big Bear'),
        ('Shower Houses', 'Shower Houses')
        )

    # these are or testing and just a place we can grab the selections
    CLARK_ROOMS = (
        ('Room 1-1', 'Room 1-1'),
        ('Room 2-1', 'Room 2-1'),
        ('Room 3-1', 'Room 3-1'),
    )

    TURNER_ROOMS = (
        ('Bear', 'Bear'),
        ('Elk', 'Elk'),
        ('Lion', 'Lion'),
    )

    FELL_ROOMS = (
        ('Room A', 'Room A'),
        ('Room B', 'Room B'),
        ('Room C', 'Room C'),
    )

    CHAPEL_ROOMS = (
        ('Main Room', 'Main Room'),
        ("Men's Bathroom", "Men's Bathroom"),
        ("Women's Bathroom", "Womens's Bathroom"),
    )

    KINSER_ROOMS = (
        ('Room 123', 'Room 123'),
        ('Room 234', 'Room 234'),
        ('Room 345', 'Room 345'),
    )

    BIGBEAR_ROOMS = (
        ('Main Room', 'Main Room'),
        ('Living Room', 'Living Room'),
        ('Bathroom', 'Bathroom'),
    )

    SHOWERHOUSE_ROOMS = (
        ('Shower A', 'Shower A'),
        ('Shower B', 'Shower B'),
        ('Shower C', 'Shower C'),
    )

    ROOMS = {
        'Clark': CLARK_ROOMS,
        'Turner': TURNER_ROOMS,
        'Fell': FELL_ROOMS,
        'Chapel': CHAPEL_ROOMS,
        'Kinser': KINSER_ROOMS,
        'Big Bear': BIGBEAR_ROOMS,
        'Shower Houses': SHOWERHOUSE_ROOMS,
    }

    location = models.CharField(max_length=200, choices=BUILDINGS)

    # these choices will change dynamically based on building information
    # NOTE: in order to do this don't set the choices field
    sub_location = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    TYPE_OF_ISSUE = (
        ('Plumbing', 'Plumbing'),
        ('Electrical', 'Electrical'),
        ('Furniture', 'Furniture'),
        ('Structural', 'Structural'),
        ('Other', 'Other - Please Explain'),
    )

    type_of_issue = models.CharField(max_length=200, choices=TYPE_OF_ISSUE)
    assigned_worker = models.CharField(max_length=200, blank=True)  # optional
    is_closed = models.BooleanField(default=False)

    # this is how you do a photo from computer in django
    # photo = models.ImageField(upload_to=f'requestPhotos/')

    # we acutally want to save all photos we upload for one requests so we can keep a history of them.
    # to do this use a one to many

    def __str__(self):
        # to get the human readable format for a choice use get_VARIABLE_display
        returnString = f'{self.task_number} - {self.location} - {self.type_of_issue}'
        return returnString

    def get_absolute_url(self):
        return reverse('workrequest-detail', args=[str(self.id)])


class WorkRequestImage(models.Model):
    # one to many for images
    request = models.ForeignKey(WorkRequest, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='qrc_app/request_photos/')

    def __str__(self):
        return f"Photo for {self.request.task_number}"

    # just in case we need this but I doubt it
    def get_absolute_url(self):
        return reverse('image-detail', args=[str(self.id)])

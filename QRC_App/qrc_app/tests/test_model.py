from django.test import TestCase
from qrc_app.models import *
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


# model tests
class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser')

        self.workRequest = WorkRequest.objects.create(
            task_number=99,
            submitter_name='Test User',
            contact_info='test@gmail.com',
            location='Kinser',
            sub_location='Room 1-1',
            description='This is a test description',
            type_of_issue='Structural',
            close_note='This issue is now closed.'
        )

        # this link helps with uploading an image https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield#26307916
        # Example using SimpleUploadedFile with actual image data

        testPhoto = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('/Users/adamsmith/Downloads/red panda.jpeg', 'rb').read(),
            content_type='image/jpeg'
        )

        self.workRequestImage = WorkRequestImage.objects.create(
            request=self.workRequest,
            photo=testPhoto
        )

    # model tests
    def testRequestCreation(self):
        self.assertEqual(self.workRequest.task_number, 99)
        self.assertEqual(self.workRequest.submitter_name, 'Test User')
        self.assertEqual(self.workRequest.contact_info, 'test@gmail.com')
        self.assertEqual(self.workRequest.location, 'Kinser')
        self.assertEqual(self.workRequest.sub_location, 'Room 1-1')
        self.assertEqual(self.workRequest.description, 'This is a test description')
        self.assertEqual(self.workRequest.type_of_issue, 'Structural')
        self.assertEqual(self.workRequest.close_note, 'This issue is now closed.')

        self.assertEqual(str(self.workRequest), f'{self.workRequest.task_number} - {self.workRequest.location} - {self.workRequest.type_of_issue}')
        self.assertEqual(self.workRequest.get_absolute_url(), f'/workrequest/{self.workRequest.pk}')

    def testWorkRequestImageCreation(self):
        self.assertEqual(self.workRequestImage.request.task_number, self.workRequest.task_number)
        self.assertIn('test_image', self.workRequestImage.photo.name)  # use this instead just in case Django changes the path to something

        self.assertEqual(str(self.workRequestImage), f"Photo for {self.workRequest.task_number}")

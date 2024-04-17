from django.test import TestCase
from qrc_app.forms import *


# form tests
class WorkRequestFormTestCase(TestCase):
    def testValidForm(self):
        data = {'submitter_name': 'John Doe',
                'contact_info': 'jdoe@uccs.edu',
                'location': 'Clark',
                'sub_location': 'Room 1-1',
                'type_of_issue': 'Electrical',
                'description': 'This is a description.',
                }
        form = WorkRequestForm(data=data)
        self.assertTrue(form.is_valid())

    def test_noName_Form(self):
        # leave out name
        data = {'contact_info': 'jdoe@uccs.edu',
                'location': 'Clark',
                'sub_location': 'Room 1-1',
                'type_of_issue': 'Electrical',
                'description': 'This is a description.',
                }
        form = WorkRequestForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('submitter_name', form.errors)
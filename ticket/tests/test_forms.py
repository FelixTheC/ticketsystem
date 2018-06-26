from django.test import TestCase

from projects.models import Project
from staff.models import Staff
from ticket.forms import TicketForm
from ticket.models import Prioritaet


class FormTestCase(TestCase):

    def setUp(self):
        Prioritaet.objects.create(name='Normal')
        Project.objects.create(name='test')
        Staff.objects.create(name='test',
                             initialies='tt',
                             email='test@test.com',
                             loginname='test',
                             accessinvoice=False,
                             accessstatistics=False
                             )

    def test_ticket_form_valid(self):
        staff = Staff.objects.get(name='test')
        form = TicketForm(data={
            'subject': 'test',
            'project': 1, # value=1 from select field
            'from_email': staff,
            'comment': 'help',
            'file': '',
        })
        self.assertTrue(form.is_valid())

    def test_ticket_form_invalid(self):
        form = TicketForm(data={
            'subject': '',
            'from_email': '',
            'comment': 'help',
            'file': '',
        })
        self.assertFalse(form.is_valid())
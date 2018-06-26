from datetime import datetime
from datetime import timedelta
from django.test import TestCase

from projects.models import Project
from staff.models import Staff
from ticket.models import Ticket
from ticket.models import Prioritaet


class TicketTestCase(TestCase):

    def setUp(self):
        Staff.objects.create(name='test',
                             initialies='tt',
                             email='test@test.com',
                             loginname='test',
                             accessinvoice=False,
                             accessstatistics=False
                             )

    def create_prio_obj(self):
        return Prioritaet.objects.create(name='normal')

    def create_project_obj(self):
        return Project.objects.create(name='test')

    def create_ticket_obj(self):
        project = self.create_project_obj()
        staff = Staff.objects.get(name='test')
        return Ticket.objects.create(subject='Test',
                                     project=project,
                                     from_email=staff.initialies,
                                     comment='Test as test',
                                     finished_until=datetime.now() + timedelta(days=30),
                                     )

    def test_true_ticket(self):
        ticket = self.create_ticket_obj()
        self.assertTrue(isinstance(ticket, Ticket))
        self.assertEqual(ticket.subject, 'Test')

    def test_str_method(self):
        ticket = self.create_ticket_obj()
        self.assertTrue(isinstance(ticket, Ticket))
        self.assertEqual(ticket.__str__(), ticket.subject)

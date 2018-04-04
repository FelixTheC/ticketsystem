import datetime
from django.test import TestCase
from ..models import Ticket
from ..models import Prioritaet

# Create your tests here.
class TicketTestCase(TestCase):

    def setUp(self):
        prioritaet = Prioritaet.objects.create(name='normal')
        ticket = Ticket.objects.create(subject='Test',
                                       from_email='test@test.com',
                                       comment='Test as test',
                                       prioritaet=prioritaet.objects.get(name='normal'),
                                       created_at=datetime.date.today()
                                       )

    def test_true_ticket(self):
        ticket = Ticket.objects.get(subject='Test')
        self.assertTrue(ticket)
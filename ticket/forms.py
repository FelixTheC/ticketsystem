from django import forms
from staff.models import Staff
from .models import Ticket, Prioritaet


STAFFS = set()
STAFFS.add(('', ''))
for staff in Staff.objects.all():
    STAFFS.add((staff.initialies, staff.name))


class PrioForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['subject', 'from_email', 'comment', 'file', 'progress', 'done', 'created_at']


class DoneForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['subject', 'from_email', 'comment', 'file', 'prioritaet', 'progress', 'created_at']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['progress', 'done', 'assigned_to']
        titles = {
            'from_email': 'Staff'
        }
        widgets = {
            'subject': forms.TextInput(attrs={'required': True}),
            'from_email': forms.Select(choices=STAFFS, attrs={'required': True}),
            'comment': forms.Textarea(attrs={'required': True,
                                             'rows': 20,
                                             'cols': 80, }),
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
            'created_at': forms.TextInput(attrs={'readonly': 'readonly',
                                                 'required': False,
                                                 'id': 'created_at'}),
        }

        help_texts = {
            'project': 'The project in which the error occurse',
            'subject': 'Title of the problem',
        }

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['prioritaet'].initial = Prioritaet.objects.get(name='Normal')

    def clean(self):
        cleaned_data = super(TicketForm, self).clean()
        from_email = cleaned_data.get('from_email')

        if from_email is not None:
            if from_email == '':
                self.add_error('from_email', 'Please select your name from the list')


class ProgressForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['subject', 'from_email', 'file', 'prioritaet', 'comment', 'done', 'created_at']
        widgets = {
            'progress': forms.Textarea(),
        }

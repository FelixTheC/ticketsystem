import os
import urllib
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, CreateView
from staff.models import Staff
from ticket.utils import searching
from ticketsystem.settings import BASE_DIR
from .models import Ticket, Prioritaet
from .models import DjangoMailboxMessage
from .models import DjangoMailboxMessageattachment
from .forms import PrioForm
from .forms import ProgressForm
from .forms import TicketForm
from .forms import DoneForm


def handle_uploaded_file(f, filepath, filename):
    if not os.path.isdir(BASE_DIR + '/media/' + filepath):
        os.mkdir(os.path.join(BASE_DIR + '/media/',  filepath))
    else:
        with open('media/' + filepath + filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()


def create_tickets():
    mails = DjangoMailboxMessage.objects.all()
    for mail in mails:
        try:
            Ticket.objects.get(mail_id=mail.id)
        except ObjectDoesNotExist:
            obj = Ticket()
            obj.mail = DjangoMailboxMessage.objects.get(id=mail.id)
            try:
                obj.attachment = DjangoMailboxMessageattachment.objects.get(message=DjangoMailboxMessage.objects.get(id=mail.id))
            except ObjectDoesNotExist:
                pass
            obj.prioritaet = Prioritaet.objects.get(name='Normal')
            obj.done = False
            obj.save()


def ticket_list(request):
    tickets = Ticket.objects.exclude(done=True)
    context = {
        'tickets': tickets,
        'done': False,
    }
    return render(request, 'list.html', context)


def ticket_done_list(request):
    tickets = Ticket.objects.exclude(done=False)
    context = {
        'tickets': tickets,
        'done': True,
    }
    return render(request, 'list.html', context)


def ticket_search(request, path):
    searchtext = request.POST['searchtext']
    tickets = Ticket.objects.none()
    done = True
    if path == '/overview/':
        done = False

    if searchtext == '':
        return redirect(reverse('ticket:list'))
    else:
        tmp = searching(Ticket, searchtext)
        for i in tmp:
            i = i.filter(done=done)
            tickets = i | tickets  # merge Querysets
    context = {
        'tickets': tickets,
        'done': done,
    }
    return render(request, 'list.html', context)


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket.html'

    def form_valid(self, form):
        # form = TicketForm(self.request.POST)
        # for afile in self.request.FILES.getlist('file'):
        #     path = str(self.request.POST['subject']) + '/'
        #     handle_uploaded_file(afile, path, str(afile))
        return super(TicketCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ticket:list')


class PrioUpdateView(UpdateView):
    model = Ticket
    template_name = 'list.html'
    form_class = PrioForm

    def get_success_url(self):
        return reverse('ticket:list')

    def form_valid(self, form):
        return super(PrioUpdateView, self).form_valid(form)


class DoneUpdateView(UpdateView):
    model = Ticket
    template_name = 'list.html'
    form_class = DoneForm

    def get_success_url(self):
        return reverse('ticket:list')

    def form_valid(self, form):
        return super(DoneUpdateView, self).form_valid(form)


class UpdateCommentView(UpdateView):
    model = Ticket
    template_name = 'ticket.html'
    fields = ('comment', 'file')
    
    def get_success_url(self):
        send_update_notice_email(self.object)
        return reverse('ticket:list')
    
    def form_valid(self, form):
        return super(UpdateCommentView, self).form_valid(form)


class ProgressUpdateView(UpdateView):
    model = Ticket
    template_name = 'list.html'
    form_class = ProgressForm

    def get_success_url(self):
        return reverse('ticket:list')

    def form_valid(self, form):
        return super(ProgressUpdateView, self).form_valid(form)


class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['form'] = ProgressForm
        return context


def download_file(request, pk):
    ticket = Ticket.objects.get(pk=pk)

    response = HttpResponse(ticket.file, content_type='application/pdf')
    response['Content-Length'] = len(ticket.file)

    original_filename = str(ticket.file).replace('file/', '')

    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % original_filename.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


def send_update_notice_email(obj):
    staff_obj = Staff.objects.get(initialies=obj.from_email)
    send_mail(
        subject=f'{obj.subject} - UPDATED',
        message=f'{obj.subject} comment or file has been updated \n\n'
                f'http://192.168.0.34:9004/admin/ticket/ticket/{obj.pk}/change/',
        from_email=staff_obj.email,
        recipient_list=['foo@bar.com', ],
        fail_silently=False
    )
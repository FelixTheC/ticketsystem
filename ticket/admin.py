from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import date
from datetime import timedelta
from staff.models import Staff
from .models import Ticket
from .models import Prioritaet

SALESINTERNMAIL = 'barfoo@foobar.com'


def send_done_mail(mail,  obj):
    staff_obj = Staff.objects.get(initialies=obj.from_email)
    it_member = User.objects.get(username=obj.assigned_to)
    send_mail(
        subject=f'{obj.subject} - DONE',
        message=f'Your Subject: {obj.subject} \n\n Your Ticketmessage:  {obj.comment} \n\n '
                f'IT-Notice:\n\n {obj.progress} \n\nWe could resolve your Problem \n\nWith best regards from  {obj.assigned_to}',
        from_email='foo@bar.com',
        recipient_list=[staff_obj.email, SALESINTERNMAIL, it_member],
        fail_silently=False
    )


def send_progress_changed_mail(mail,  obj):
    staff_obj = Staff.objects.get(initialies=obj.from_email)
    it_member = User.objects.get(name=obj.assigned_to)
    send_mail(
        subject=f'{obj.subject} -CHANGED',
        message=f'IT comment/progress has changed at {obj.changed_timestamp}: \n\n{obj.progress}\n\n',
        from_email=it_member,
        recipient_list=[staff_obj.email, SALESINTERNMAIL],
        fail_silently=False
    )


def send_prioritaet_changed_mail(mail,  obj):
    staff_obj = Staff.objects.get(initialies=obj.from_email)
    it_member = User.objects.get(name=obj.assigned_to)
    send_mail(
        subject=f'{obj.subject} -CHANGED',
        message=f'IT prioritaet has changed to: \n\n{obj.prioritaet}\n\n',
        from_email=it_member,
        recipient_list=[staff_obj.email, SALESINTERNMAIL],
        fail_silently=False
    )


def send_assigned_to_mail(mail,  obj):
    staff_obj = Staff.objects.get(initialies=obj.from_email)
    it_member = User.objects.get(name=obj.assigned_to)
    send_mail(
        subject=f'{obj.subject} - ACCEPTED',
        message=f'{obj.subject} is assigned to: {obj.assigned_to}\n\nProgress: {obj.it_status}'
                f'\nexpected completion date: {obj.finished_until}',
        from_email=it_member,
        recipient_list=[staff_obj.email, SALESINTERNMAIL],
        fail_silently=False
    )


def make_done(modeladmin, request, queryset):
    queryset.update(done='True')
    for query in queryset:
        send_done_mail(query)


make_done.short_description = 'Mark selected Tickets as Done'


class TicketAdmin(admin.ModelAdmin):
    list_display = ['done', 'project', 'subject', 'from_email', 'prioritaet', 'assigned_to', 'created_at', 'finished_until']
    list_display_links = ['done', 'project', 'subject', ]
    list_filter = ['done', 'prioritaet', 'from_email', 'project', 'created_at', 'finished_until']
    actions = [make_done, ]
    readonly_fields = ['subject', 'from_email', 'comment', 'file', 'created_at', 'assigned_to', ]
    change_form_template = 'admin/change_form.html'

    def get_queryset(self, request):
        return super(TicketAdmin, self).get_queryset(request)

    def save_model(self, request, obj, form, change):
        if not obj.finished_until:
            obj.finished_until = date.today() + timedelta(days=30)
        if not obj.assigned_to:
            obj.assigned_to = request.user.username
            if obj.it_status is None:
                obj.it_status = 'In Progress'
            send_assigned_to_mail(request.user.email, obj)
        if obj.assigned_to:
            if obj.done:
                send_done_mail(request.user.email, obj)
            elif 'progress' in form.changed_data:
                send_progress_changed_mail(request.user.email, obj)
                obj.changed_timestamp = date.today()
            elif 'prioritaet' in form.changed_data:
                send_progress_changed_mail(request.user.email, obj)
        if not obj.finished_until:
            obj.finished_until = date.today() + timedelta(days=30)
        return super(TicketAdmin, self).save_model(request, obj, form, change)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Prioritaet)